#!/usr/bin/env python3
import argparse

TEMPLATES = {
    "urgent": "Dear {target},\n\nThis is an urgent notification from {company}.\nYour account has been temporarily suspended due to suspicious activity.\nPlease verify your identity by clicking the link below:\n{link}\n\nFailure to do so within 24 hours will result in account closure.\n\nRegards,\n{company} Security Team",
    "invoice": "Dear {target},\n\nPlease find attached the invoice for your recent purchase from {company}.\nThe total amount of ${amount} is due by {date}.\nIf you have any questions, contact our support team.\n\nInvoice: {link}\n\nThank you,\n{company} Billing Department",
    "password_reset": "Hello {target},\n\nWe received a request to reset your password for {company}.\nTo reset your password, please click the link below:\n{link}\n\nIf you did not request this, please ignore this email.\n\n{company} Support",
    "offer": "Dear {target},\n\nCongratulations! You have been selected for an exclusive offer from {company}.\nClaim your {offer} today by visiting:\n{link}\n\nThis offer expires soon, so act fast!\n\n{company} Team"
}

def list_templates():
    print("Available templates:")
    for name in TEMPLATES:
        print(f"  {name}")

def generate(template_name, placeholders):
    if template_name not in TEMPLATES:
        return "Template not found."
    text = TEMPLATES[template_name]
    for key, value in placeholders.items():
        text = text.replace(f"{{{key}}}", value)
    return text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Social engineering template builder")
    parser.add_argument("--list", action="store_true", help="List available templates")
    parser.add_argument("--template", help="Template name")
    parser.add_argument("--target", help="Target name")
    parser.add_argument("--company", help="Company name")
    parser.add_argument("--link", help="Phishing link")
    parser.add_argument("--amount", help="Amount for invoice")
    parser.add_argument("--date", help="Date for invoice")
    parser.add_argument("--offer", help="Offer description")
    parser.add_argument("--output", help="Save to file")
    args = parser.parse_args()
    if args.list:
        list_templates()
        sys.exit(0)
    if not args.template:
        print("Please specify --template")
        sys.exit(1)
    placeholders = {}
    if args.target: placeholders['target'] = args.target
    if args.company: placeholders['company'] = args.company
    if args.link: placeholders['link'] = args.link
    if args.amount: placeholders['amount'] = args.amount
    if args.date: placeholders['date'] = args.date
    if args.offer: placeholders['offer'] = args.offer
    result = generate(args.template, placeholders)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result)
        print(f"Template saved to {args.output}")
    else:
        print(result)
