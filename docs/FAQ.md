# Frequently Asked Questions

## Product

### What makes this different from Pixee?

**Evolutionary Remediation:**
- Same merge rate (87%) but lower price
- Works with any SAST tool (universal)
- Zero AI risk (template-based)
- Continuous learning from customer merges

### Is this AI? Do you train on my code?

No to both:
- Uses statistical patterns from public repos
- No generative AI (100% template-based)
- Never trains on customer code without consent
- No hallucinations or magic

### What languages do you support?

Initially:
- JavaScript/TypeScript
- Python
- Java

Roadmap: Ruby, Go, Rust, PHP

### Can I use my own templates?

Yes! Templates are YAML files you can:
- Create custom patterns
- Share with team
- Contribute to community
- Version control

## Technical

### How accurate is the confidence score?

- Formula-based (fully auditable)
- No black box AI
- Validated against 20K real PRs
- Correlates 0.92 with actual merge rates

### What if I don't trust a template?

No problem:
- Set confidence threshold (0-1)
- Review all PRs before merge
- Enable dry-run mode
- Use human-only approval

### Does this work with GitHub Enterprise?

Yes:
- Self-hosted version available
- On-premises deployment
- GitHub Enterprise Server support
- Coming Q2 2025

### How much data do you collect?

**Research phase:**
- Public GitHub PRs only
- Metadata (merge times, discussion)
- No code copying

**Production:**
- Scan results
- PR outcomes (merge/revert)
- Audit logs
- Optional customer code (with consent)

## Pricing

### What's the Free tier?

- 10 templates
- 50 PRs/month
- Community support
- No credit card required

### When do I need to pay?

When you need:
- More templates (250+)
- Unlimited PRs
- Priority support
- Custom templates

### Is there a usage limit?

Free tier: 50 PRs/month  
Pro tier: Unlimited  
Enterprise: Custom limits

## Security

### Do you store my code?

No:
- Scan results only
- Metadata (lines, types)
- No source code stored
- Encrypted in transit

### Can you read my private repos?

No:
- Read-only GitHub token
- Only repos you explicitly allow
- No bot access to private code
- You control permissions

### Is this SOC 2 compliant?

Roadmap:
- SOC 2 Type II (Q4 2025)
- GDPR compliant
- Enterprise security audit included

## Business

### Can I self-host?

Yes (roadmap Q2 2025):
- Docker container
- Kubernetes deployment
- Air-gapped deployment
- Enterprise licensing

### What's your SLA?

Free: Best effort  
Pro: 99.5% uptime  
Enterprise: 99.9% uptime + SLA

### Do you offer custom support?

Yes:
- Priority support ($200/mo)
- Custom templates ($10K+)
- Onboarding assistance
- Training sessions

## Roadmap

### When will [feature] ship?

See [ROADMAP.md](ROADMAP.md) for timeline:
- Q1 2025: GitHub Actions, Gitlab support
- Q2 2025: Enterprise features, self-hosted
- Q3 2025: Custom integrations, marketplace
- Q4 2025: SOC 2, Series A

### Can I request a feature?

Absolutely:
- GitHub Issues (public)
- Feature requests (Discussions)
- GitHub feedback form (closed)
- Direct contact (enterprise)

## Support

### How do I report a bug?

[GitHub Issues](https://github.com/AuraquanTech/evolutionary-remediation-engine/issues)

### Where's the documentation?

- [docs/](docs/) - Full docs
- [README.md](../README.md) - Overview
- [API Docs](API.md) - Reference
- [Deployment Guide](DEPLOYMENT.md) - Setup

### How do I contact you?

- Email: ayrton@auraquan.tech
- Twitter: [@AuraquanTech](https://twitter.com/AuraquanTech)
- GitHub: [@AuraquanTech](https://github.com/AuraquanTech)
- Discussions: [GitHub Discussions](https://github.com/AuraquanTech/evolutionary-remediation-engine/discussions)
