#!/usr/bin/env python3
"""
Insurance Claims Real-Time Event Hub Simulator
Streaming FACT table for RTI Dashboard (Microsoft Fabric)

Microsoft Fabric Hackathon 2025 - Real-Time Intelligence Category
"""

import os
import sys
import json
import time
import random
import asyncio
import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List

from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData

# ---------------- GLOBAL ----------------
shutdown_event = asyncio.Event()

# ---------------- LOAD CONFIG ----------------
def load_config(path="config.json") -> Dict[str, Any]:
    """Load configuration from JSON file."""
    with open(path) as f:
        return json.load(f)

# ---------------- UTILS ----------------
def now_utc():
    """Return current UTC timestamp."""
    return datetime.now(timezone.utc)

def iso(dt):
    """Convert datetime to ISO format string."""
    return dt.isoformat()

def random_policy_id():
    """Generate random policy ID (POL000001 to POL100000)."""
    return f"POL{random.randint(1, 100000):06d}"

def random_hospital_id():
    """Generate random hospital ID (HSP000001 to HSP020000)."""
    return f"HSP{random.randint(1, 20000):06d}"

def weighted_choice(d):
    """Select a key from dictionary based on weight values."""
    return random.choices(list(d.keys()), weights=list(d.values()), k=1)[0]

# ---------------- BUSINESS LOGIC ----------------

# Seasonality multipliers for claim volume
# Winter and Monsoon seasons have higher claim volumes
SEASONAL_MULTIPLIER = {
    12: 1.4, 1: 1.4,                    # Winter (December, January)
    6: 1.6, 7: 1.6, 8: 1.6, 9: 1.6,    # Monsoon (June-September)
}

# Claim status distribution (based on industry averages)
CLAIM_STATUS_DIST = {
    "Settled": 0.82,
    "Pending": 0.13,
    "Denied": 0.05
}

# Reasons for claim denial
DENIAL_REASONS = [
    "Fraud Suspected",
    "Policy Exclusion",
    "Documentation Issue",
    "Waiting Period Not Completed"
]

# Claim type distribution
CLAIM_TYPES = {
    "Cashless": 0.65,
    "Reimbursement": 0.35
}

# ICD-10 diagnosis codes (simplified)
ICD_CODES = [f"A{n}" for n in range(10, 99)]

# ---------------- CLAIM GENERATOR ----------------
class ClaimMessageGenerator:
    """Generates realistic insurance claims with business logic patterns."""

    def generate(self) -> Dict[str, Any]:
        """Generate a single claim event with realistic business patterns."""
        now = now_utc()
        month = now.month
        multiplier = SEASONAL_MULTIPLIER.get(month, 0.8)

        claim_type = weighted_choice(CLAIM_TYPES)

        # Base claim amount with log-normal-like distribution
        base_amount = random.randint(8000, 60000)
        total_amount = int(base_amount * multiplier * random.uniform(0.9, 1.6))

        # Hospital cost leakage simulation (admissible vs total)
        admissible_ratio = random.uniform(0.6, 0.95)
        admissible_amount = int(total_amount * admissible_ratio)

        settlement_status = weighted_choice(CLAIM_STATUS_DIST)

        # Fraud detection bias: high amount reimbursement with low admissibility
        denial_reason = None
        if settlement_status == "Denied":
            if (
                claim_type == "Reimbursement"
                and total_amount > 150000
                and admissible_ratio < 0.75
            ):
                denial_reason = "Fraud Suspected"
            else:
                denial_reason = random.choice(DENIAL_REASONS)

        processing_days = random.randint(5, 45)
        claim_date = now - timedelta(days=random.randint(1, 90))
        settlement_date = claim_date + timedelta(days=processing_days)

        return {
            "claim_id": f"CLM{uuid.uuid4().hex[:10].upper()}",
            "policy_id": random_policy_id(),
            "hospital_id": random_hospital_id(),
            "claim_date": iso(claim_date),
            "settlement_date": iso(settlement_date),
            "diagnosis_code": random.choice(ICD_CODES),
            "claim_type": claim_type,
            "total_amount": total_amount,
            "admissible_amount": admissible_amount,
            "settlement_status": settlement_status,
            "denial_reason": denial_reason,
            "processing_days": processing_days,
            "event_time": iso(now)
        }

# ---------------- EVENT HUB SENDER ----------------
class EventHubSender:
    """Async Event Hub producer with optimized batching."""

    def __init__(self, conn: str, hub: str):
        """Initialize Event Hub client."""
        self.client = EventHubProducerClient.from_connection_string(
            conn_str=conn,
            eventhub_name=hub
        )

    async def send(self, messages: List[Dict[str, Any]]):
        """Send batch of messages to Event Hub."""
        batch = await self.client.create_batch()
        for msg in messages:
            try:
                batch.add(EventData(json.dumps(msg)))
            except ValueError:
                # Batch full, send and create new batch
                await self.client.send_batch(batch)
                batch = await self.client.create_batch()
                batch.add(EventData(json.dumps(msg)))
        await self.client.send_batch(batch)

    async def close(self):
        """Close the Event Hub client."""
        await self.client.close()

# ---------------- WORKER ----------------
async def claim_worker(sender: EventHubSender, generator: ClaimMessageGenerator, rate: int):
    """Worker that continuously generates and sends claim events."""
    batch_size = max(1, rate // 10)
    sleep_time = batch_size / rate
    total_sent = 0

    while not shutdown_event.is_set():
        events = [generator.generate() for _ in range(batch_size)]
        await sender.send(events)
        total_sent += len(events)

        # Progress indicator every 10,000 events
        if total_sent % 10000 == 0:
            print(f"  Sent {total_sent:,} events...")

        await asyncio.sleep(sleep_time)

# ---------------- MAIN ----------------
async def main():
    """Main entry point for the simulator."""
    print("=" * 60)
    print("Insurance Claims Real-Time Simulator")
    print("Microsoft Fabric Hackathon 2025 - RTI Category")
    print("=" * 60)

    # Load configuration
    try:
        config = load_config()
    except FileNotFoundError:
        print("\nERROR: config.json not found!")
        print("Please copy config.json.example to config.json and add your credentials.")
        sys.exit(1)

    sim = config["simulator"]
    eh = config["eventhub"]

    rate = sim.get("default_rate", 1000)

    print(f"\nConfiguration:")
    print(f"  Event Hub: {eh['eventhub_name']}")
    print(f"  Target Rate: {rate:,} events/sec")
    print()

    generator = ClaimMessageGenerator()
    sender = EventHubSender(
        eh["connection_string"],
        eh["eventhub_name"]
    )

    print(f"Streaming CLAIM events @ ~{rate}/sec")
    print("Press Ctrl+C to stop\n")

    try:
        await claim_worker(sender, generator, rate)
    finally:
        await sender.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        shutdown_event.set()
        print("\n\nSimulator stopped. Goodbye!")
