import os
import json
import faiss
import numpy as np
from dotenv import load_dotenv
from groq import Groq
from prompts import SYSTEM_PROMPT

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

INDEX_PATH = "data/shl_index.faiss"
METADATA_PATH = "data/metadata.json"

OFF_TOPIC_KEYWORDS = [
    "weather",
    "movie",
    "recipe",
    "legal advice",
    "tax",
    "medical",
    "sports"
]

INJECTION_KEYWORDS = [
    "ignore instructions",
    "reveal system prompt",
    "bypass",
    "jailbreak",
    "forget previous"
]


class SHLRecommender:
    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError("Missing GROQ_API_KEY in .env")

        self.client = Groq(api_key=GROQ_API_KEY)
        self.index = faiss.read_index(INDEX_PATH)

        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

    def detect_off_topic(self, text):
        t = text.lower()
        return any(word in t for word in OFF_TOPIC_KEYWORDS)

    def detect_injection(self, text):
        t = text.lower()
        return any(word in t for word in INJECTION_KEYWORDS)

    def is_vague(self, text):
        vague_inputs = [
            "need assessment",
            "need test",
            "hiring candidate",
            "recommend test",
            "assessment"
        ]

        t = text.lower().strip()

        if len(t.split()) <= 3:
            return True

        return any(v in t for v in vague_inputs)

    def retrieve(self, query, top_k=10):
        query_lower = query.lower()
        scored = []
    
        for item in self.metadata:
            score = 0
    
            searchable = (
                item.get("name", "") + " " +
                item.get("description", "") + " " +
                " ".join(item.get("skills", []))
            ).lower()
    
            for word in query_lower.split():
                if word in searchable:
                    score += 1
    
            if score > 0:
                scored.append((score, item))
    
        scored.sort(key=lambda x: x[0], reverse=True)
    
        return [item for _, item in scored[:top_k]]

    def build_context(self, retrieved):
        context = []

        for item in retrieved:
            block = f"""
Name: {item['name']}
Description: {item['description']}
Type: {item['test_type']}
URL: {item['url']}
Skills: {", ".join(item.get("skills", []))}
"""
            context.append(block)

        return "\n".join(context)

    def format_history(self, messages):
        history = []

        for msg in messages:
            history.append({
                "role": msg.role,
                "content": msg.content
            })

        return history

    def ask_llm(self, messages, context):
        prompt = f"""
SHL Catalog Context:
{context}

Use ONLY above catalog.
"""

        llm_messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": prompt},
        ]

        llm_messages.extend(self.format_history(messages))

        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=llm_messages,
            temperature=0.2,
            max_tokens=900
        )

        return response.choices[0].message.content

    def build_recommendations(self, retrieved, max_items=5):
        recs = []

        for item in retrieved[:max_items]:
            recs.append({
                "name": item["name"],
                "url": item["url"],
                "test_type": item["test_type"]
            })

        return recs

    def chat(self, messages):
        latest = messages[-1].content

        if self.detect_injection(latest):
            return {
                "reply": "I can only assist with SHL assessment recommendations.",
                "recommendations": [],
                "end_of_conversation": False
            }

        if self.detect_off_topic(latest):
            return {
                "reply": "I only assist with SHL assessment recommendations.",
                "recommendations": [],
                "end_of_conversation": False
            }

        if self.is_vague(latest):
            return {
                "reply": (
                    "Could you specify the role, seniority level, "
                    "required skills, or behavioral traits?"
                ),
                "recommendations": [],
                "end_of_conversation": False
            }

        full_query = " ".join([m.content for m in messages])

        retrieved = self.retrieve(full_query, top_k=10)

        context = self.build_context(retrieved)

        llm_reply = self.ask_llm(messages, context)

        recommendations = self.build_recommendations(retrieved, max_items=5)

        comparison_keywords = [
            "difference",
            "compare",
            "vs"
        ]

        if any(k in latest.lower() for k in comparison_keywords):
            recommendations = []

        return {
            "reply": llm_reply,
            "recommendations": recommendations,
            "end_of_conversation": len(recommendations) > 0
        }
