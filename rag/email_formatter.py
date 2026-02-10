# def clean_llm_text(text: str) -> str:
#     # Remove extra blank lines
#     lines = [line.strip() for line in text.splitlines() if line.strip()]

#     # Join cleanly
#     cleaned = "<br>".join(lines)

#     return cleaned


# def format_daily_email(results):
#     html = """
#     <html>
#     <body style="font-family: Arial, sans-serif; line-height: 1.6;">
#     <h2 style="color:#1a237e;">📰 UPSC Daily Current Affairs – Top 5</h2>
#     <hr>
#     """

#     for i, r in enumerate(results, 1):
#         html += f"""
#         <div style="margin-bottom: 35px;">
        
#         <h3 style="margin-bottom:5px;">{i}. {r['title']}</h3>   

#         <p style="margin:4px 0;">
#             <b>Source:</b> {r['source']} <br>
#             <b>Article:</b> 
#             <a href="{r['url']}" target="_blank">{r['url']}</a><br>
#             <b>Priority:</b> 
#             <span style="color:{'red' if r['priority']=='HIGH' else 'orange'};">
#                 {r['priority']}
#             </span><br>
#             <b>PYQ Linkage:</b> {r.get('pyq_status', '—')}
#         </p>

#         <div style="background:#f9f9f9; padding:12px; border-left:4px solid #1a237e;">
#             <p>{clean_llm_text(r['summary'])}</p>

#         </div>
#         <ul>
#         """

#         html += """
#         </ul>
#         <hr style="margin-top:25px;">
#         </div>
#         """

#     html += "</body></html>"
#     return html

import re

import re

def clean_text(text: str) -> str:
    if not text:
        return ""

    # Split lines & strip whitespace
    lines = [l.strip() for l in text.splitlines()]

    normalized = []
    for l in lines:
        # Drop empty lines completely
        if l == "":
            continue

        # Normalize bullets
        l = re.sub(r'^[•\-–—]\s*', '– ', l)

        normalized.append(l)

    text = "\n".join(normalized)

    # Tighten section headers spacing
    text = re.sub(r'(Summary|Facts|Material|Introduction|Body|Conclusion|Way Forward)\s*:', r'\1:', text)

    # Convert to HTML breaks
    return text.replace("\n", "<br>")



def format_daily_email(results):
    html = """
    <html>
    <body style="font-family: Arial, sans-serif; line-height:1.6;">
    <h2>📰 UPSC Daily Current Affairs – Top 25</h2>
    <hr>
    """

    for i, r in enumerate(results, 1):
        html += f"""
        <h3>{i}. {r['title']}</h3>

        <b>Source:</b> {r['source']}<br>
        <b>Article:</b> <a href="{r['url']}">{r['url']}</a><br>
        <b>Priority:</b> {r['priority']}<br>
        <b>PYQ Linkage:</b> {r.get('pyq_status', '—')}<br><br>

        {clean_text(r['summary'])}

        <br><br>
        <b>Syllabus Linkage:</b>
        <ul>
        """

        # for s in r["syllabus"]:
        #     topic = s.get("topic") or s.get("paper") or s.get("title")
        #     if topic:
        #         html += f"<li>{topic}</li>"
        for s in r["syllabus"]:
            html += f"<li>{s['gs']} – {s['topic']}</li>"


        html += """
        </ul>
        <hr>
        """

    html += "</body></html>"
    return html
