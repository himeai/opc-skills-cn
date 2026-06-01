#!/usr/bin/env python3
"""icp-domain-cn: 综合判断本次上线要办什么备案 / 资质.

Input:  "subject=individual|domain=example.com|hosting=cn_mainland"
Output: JSON {decisions, advice, common_rejections}
"""

from __future__ import annotations

from cli_common import load_ref, require, run_kv_cli  # type: ignore[import-not-found]


def _domain_suffix(domain: str) -> str:
    """Map a domain to a known suffix key."""
    d = domain.lower().strip()
    if d.endswith(".com.cn"):
        return "com_cn"
    if d.endswith(".cn"):
        return "cn"
    if d.endswith(".com"):
        return "com"
    if d.endswith(".net"):
        return "net"
    if d.endswith(".io") or d.endswith(".dev"):
        return "io_dev"
    return "com"


def build_check(fields: dict[str, str]) -> dict:
    """Decide what filings & qualifications are needed for this site."""
    subject, domain, hosting = require(fields, "subject", "domain", "hosting")
    rules = load_ref("rules")

    if subject not in rules["subject_types"]:
        raise ValueError(f"unknown subject '{subject}'")
    if hosting not in rules["hosting_choice"]:
        raise ValueError(f"unknown hosting '{hosting}'")

    sub_meta = rules["subject_types"][subject]
    host_meta = rules["hosting_choice"][hosting]
    suffix = _domain_suffix(domain)
    dom_meta = rules["domain_suffix_rules"].get(suffix, {})

    icp_required = host_meta["requires_icp_filing"]
    psb_required = host_meta["requires_psb_filing"]
    real_name_required = bool(dom_meta.get("requires_real_name"))

    advice: list[str] = []
    advice.append(f"主体类型：{sub_meta['label']}。{sub_meta['note']}")
    advice.append(f"服务器：{host_meta['label']}。"
                  f"优点：{', '.join(host_meta['pros'])}；"
                  f"缺点：{', '.join(host_meta['cons'])}")
    if dom_meta:
        advice.append(f"域名后缀 .{suffix.replace('_', '.')}：{dom_meta.get('note', '')}")
    if icp_required:
        advice.append("→ 必须完成 ICP 备案；详见 steps.py filing=icp")
    else:
        advice.append("→ 当前服务器选择不需要 ICP 备案；如启用国内 CDN 仍需备案")
    if psb_required:
        advice.append("→ 必须完成公安备案（拿到 ICP 备案号后 30 天内）；详见 steps.py filing=psb")
    if real_name_required:
        advice.append("→ 域名必须实名认证（注册商后台办理）")
    if subject == "individual" and hosting == "cn_mainland":
        advice.append("→ 个人主体备案站点严禁经营性内容（电商 / 付费内容 / 广告联盟）")

    return {
        "subject": subject,
        "domain": domain,
        "domain_suffix": suffix,
        "hosting": hosting,
        "decisions": {
            "icp_filing_required": icp_required,
            "psb_filing_required": psb_required,
            "domain_real_name_required": real_name_required,
        },
        "advice": advice,
        "common_rejections": rules["common_rejections"],
    }


def main() -> int:
    """Entry point for check.py."""
    return run_kv_cli(
        'check.py "subject=individual|individual_business|company'
        '|domain=X|hosting=cn_mainland|hk_macao|overseas"',
        build_check,
    )


if __name__ == "__main__":
    raise SystemExit(main())
