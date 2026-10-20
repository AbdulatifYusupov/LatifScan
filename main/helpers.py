"""Shared helpers for views."""

import hashlib

from django.http import JsonResponse

from .models import ScanResult


def get_client_ip(request) -> str:
    x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded:
        return x_forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def get_file_sha256(uploaded_file) -> str:
    hasher = hashlib.sha256()
    for chunk in uploaded_file.chunks():
        hasher.update(chunk)
    uploaded_file.seek(0)
    return hasher.hexdigest()


def extract_engines(raw_result) -> list[dict]:
    """Pull per-engine verdicts from VirusTotal raw JSON."""
    if not raw_result or not isinstance(raw_result, dict):
        return []

    data = raw_result.get("data") or {}
    attrs = data.get("attributes") or {}
    results = attrs.get("results") or attrs.get("last_analysis_results") or {}
    if not isinstance(results, dict):
        return []

    engines = []
    for name, info in results.items():
        if not isinstance(info, dict):
            continue
        category = (info.get("category") or "undetected").lower()
        engines.append({
            "engine": name,
            "category": category,
            "result": info.get("result") or category,
        })

    order = {"malicious": 0, "suspicious": 1, "harmless": 2, "undetected": 3, "timeout": 4, "type-unsupported": 5, "failure": 6}
    engines.sort(key=lambda e: (order.get(e["category"], 99), e["engine"].lower()))
    return engines


def build_response(scan: ScanResult) -> dict:
    """Serialize ScanResult to JSON for the frontend."""
    engines = extract_engines(scan.raw_result)
    return {
        "id": scan.id,
        "scan_type": scan.scan_type,
        "status": scan.status,
        "verdict": getattr(scan, "verdict", None),
        "danger_percent": getattr(scan, "danger_percent", 0),
        "malicious": scan.malicious_count,
        "suspicious": scan.suspicious_count,
        "harmless": scan.harmless_count,
        "undetected": scan.undetected_count,
        "total_engines": scan.total_engines,
        "is_phishing": scan.is_phishing,
        "url": scan.url,
        "file_name": scan.file_name,
        "file_hash": scan.file_hash_sha256,
        "file_size": scan.file_size,
        "created_at": scan.created_at.strftime("%d.%m.%Y %H:%M"),
        "engines": engines,
        "export_url": f"/scan/{scan.id}/export/" if scan.id else None,
    }


def error_response(message: str, status: int = 400) -> JsonResponse:
    return JsonResponse({"error": message}, status=status)
