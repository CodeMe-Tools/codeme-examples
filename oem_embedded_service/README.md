# Codeme OEM Embedded Service Example

Demonstrates how third-party tools, IDE extensions, or autonomous CI review agents embed the Codeme verification platform without CLI presentation logic.

## Usage

```python
from oem_embedded_service.embedded_bot import AutonomousReviewBot

bot = AutonomousReviewBot()
report = bot.review_submission(target_path="path/to/code", fix=True)

print(f"Review verdict: {report['verdict']}")
print(f"Tokens saved: {report['token_metrics']['estimated_tokens_saved']}")
```
