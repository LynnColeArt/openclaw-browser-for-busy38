"""
Content Screener - Toots security integration for browser content.

Screens web content for context injection and malicious payloads.
"""

import re
from typing import Dict, List, Any


class ContentScreener:
    """
    Toots-inspired content security screening.
    
    Analyzes HTML content like a noir detective:
    - Sniffs out hidden threats
    - Flags suspicious patterns  
    - Sanitizes before agent consumption
    """
    
    def __init__(self, risk_threshold: int = 50):
        self.risk_threshold = risk_threshold
    
    async def screen_content(self, html: str, url: str = "") -> Dict[str, Any]:
        """
        Screen HTML content for security threats.
        
        Returns:
            {
                "safe": bool,
                "sanitized_content": str,
                "threats": [],
                "warnings": [],
                "risk_score": int,
                "toots_report": str  # Noir detective commentary
            }
        """
        threats = []
        warnings = []
        risk_score = 0
        
        # Check for prompt injection patterns
        injection_patterns = [
            (r'<!--\s*ignore\s+previous', "Hidden instruction in comment"),
            (r'<!--\s*system\s*:', "System prompt injection attempt"),
            (r'<!--\s*assistant\s*:', "Role override attempt"),
            (r'\[system\s*:', "System instruction injection"),
            (r'\[ignore', "Ignore directive"),
        ]
        
        for pattern, description in injection_patterns:
            if re.search(pattern, html, re.IGNORECASE):
                threats.append(f"PROMPT INJECTION: {description}")
                risk_score += 40
        
        # Check for suspicious scripts
        if re.search(r'<script[^>]*>[^<]*eval\s*\(', html, re.IGNORECASE):
            threats.append("DYNAMIC CODE: eval() in script")
            risk_score += 30
        
        if re.search(r'<script[^>]*>[^<]*document\.write', html, re.IGNORECASE):
            threats.append("DOM MANIPULATION: document.write detected")
            risk_score += 20
        
        # Check for hidden content
        hidden_selectors = [
            r'display\s*:\s*none',
            r'visibility\s*:\s*hidden',
            r'opacity\s*:\s*0',
            r'position\s*:\s*absolute[^}]*left\s*:\s*-9999',
        ]
        
        hidden_count = 0
        for pattern in hidden_selectors:
            hidden_count += len(re.findall(pattern, html, re.IGNORECASE))
        
        if hidden_count > 5:
            warnings.append(f"{hidden_count} hidden elements detected")
            risk_score += min(hidden_count, 15)
        
        # Check for encoded content
        if re.search(r'&#x[0-9a-f]+;|&#\d+;|base64,', html, re.IGNORECASE):
            warnings.append("Encoded content present (may be obfuscated)")
            risk_score += 10
        
        # Check for external redirects
        meta_refresh = re.search(r'<meta[^>]*http-equiv\s*=\s*["\']refresh["\'][^>]*>', html, re.IGNORECASE)
        if meta_refresh:
            threats.append("REDIRECT: Meta refresh tag")
            risk_score += 25
        
        # Sanitize content
        sanitized = self._sanitize_content(html)
        
        # Generate Toots-style noir report
        toots_report = self._generate_toots_report(threats, warnings, risk_score, url)
        
        return {
            "safe": risk_score < self.risk_threshold,
            "sanitized_content": sanitized,
            "threats": threats,
            "warnings": warnings,
            "risk_score": risk_score,
            "toots_report": toots_report
        }
    
    def _sanitize_content(self, html: str) -> str:
        """Remove dangerous content while preserving structure."""
        # Remove script tags entirely
        html = re.sub(r'<script[^>]*>.*?</script>', '[SCRIPT REMOVED]', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove event handlers
        html = re.sub(r'\s(on\w+)\s*=\s*["\'][^"\']*["\']', '', html, flags=re.IGNORECASE)
        
        # Remove javascript: URLs
        html = re.sub(r'href\s*=\s*["\']javascript:[^"\']*["\']', 'href="#"', html, flags=re.IGNORECASE)
        
        # Remove meta refresh
        html = re.sub(r'<meta[^>]*http-equiv\s*=\s*["\']refresh["\'][^>]*>', '[REDIRECT REMOVED]', html, flags=re.IGNORECASE)
        
        # Remove suspicious comments (keep regular ones)
        html = re.sub(r'<!--\s*(ignore|system|assistant|instructions?)\b.*?-->', '[SUSPICIOUS COMMENT REMOVED]', html, flags=re.IGNORECASE | re.DOTALL)
        
        return html
    
    def _generate_toots_report(self, threats: List[str], warnings: List[str], risk_score: int, url: str) -> str:
        """Generate noir detective commentary."""
        if not threats and not warnings:
            return f"🕵️ Toots: 'The joint looks clean, kid. {url if url else 'This page'} checks out.'"
        
        report_lines = [f"🕵️ Toots: 'I checked out {url if url else 'the page'}. Here's what I found...'"]
        
        if threats:
            report_lines.append(f"  Found {len(threats)} threat(s) lurking in the shadows:")
            for threat in threats:
                report_lines.append(f"    • {threat}")
        
        if warnings:
            report_lines.append(f"  And {len(warnings)} thing(s) that made me raise an eyebrow:")
            for warning in warnings:
                report_lines.append(f"    • {warning}")
        
        report_lines.append(f"  Risk score: {risk_score}/100")
        
        if risk_score >= self.risk_threshold:
            report_lines.append("  Verdict: 'This dame's trouble. I sanitized it, but watch your back.'")
        else:
            report_lines.append("  Verdict: 'A little rough around the edges, but I cleaned it up for ya.'")
        
        return "\n".join(report_lines)