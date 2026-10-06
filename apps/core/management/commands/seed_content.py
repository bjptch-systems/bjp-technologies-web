from django.core.management.base import BaseCommand

from apps.industries.models import Industry
from apps.services.models import Service

SERVICES = [
    {
        "name": "Software Development",
        "slug": "software-development",
        "tagline": "Custom software built for East African businesses",
        "order": 1,
        "icon_svg": "22.svg",
        "image": "bjp-software-development.webp",
        "description": (
            "We design and build custom software that fits exactly how your business works — "
            "not the other way around. From ERP systems and payroll platforms to loan management "
            "and point-of-sale systems, we deliver robust, maintainable solutions built with "
            "PHP and Laravel. Our team handles everything from requirements through deployment "
            "and ongoing support."
        ),
        "bullet_points": (
            "Custom Web Applications (PHP, Laravel)\n"
            "Enterprise Systems — ERP, HR, Payroll, Accounting\n"
            "Loan Management & Financial Systems (SACCOS, Microfinance)\n"
            "Inventory, POS & Billing Systems\n"
            "API Development & Third-Party Integrations"
        ),
    },
    {
        "name": "Website & Digital Solutions",
        "slug": "website-digital-solutions",
        "tagline": "Professional digital presence for your organisation",
        "order": 2,
        "icon_svg": "23.svg",
        "image": "bjp-website-digital-solutions.webp",
        "description": (
            "Your website is your most visible business asset. We build corporate websites, "
            "e-commerce platforms, and content management systems that are fast, secure, and "
            "easy to manage. Every site we deliver is mobile-responsive, SEO-ready, and "
            "optimised for performance — so your organisation makes the right first impression."
        ),
        "bullet_points": (
            "Corporate & Institutional Websites\n"
            "E-Commerce Platforms\n"
            "Content Management Systems (CMS)\n"
            "Website Maintenance & Performance Optimisation"
        ),
    },
    {
        "name": "Cloud & Infrastructure",
        "slug": "cloud-infrastructure",
        "tagline": "Scalable, reliable infrastructure on leading cloud platforms",
        "order": 3,
        "icon_svg": "24.svg",
        "image": "bjp-cloud-infrastructure.webp",
        "description": (
            "We design, deploy, and manage cloud infrastructure on AWS, Oracle Cloud, and "
            "DigitalOcean — giving your business the reliability and scalability you need to "
            "grow without worrying about servers. Our Linux administration team handles "
            "everything from initial setup through ongoing management, backups, and "
            "disaster recovery."
        ),
        "bullet_points": (
            "Cloud Server Setup — AWS, Oracle Cloud, DigitalOcean\n"
            "Linux Server Administration — AlmaLinux, Ubuntu\n"
            "cPanel / WHM Management\n"
            "Backup & Disaster Recovery Solutions\n"
            "High Availability & Performance Optimisation"
        ),
    },
    {
        "name": "Cybersecurity",
        "slug": "cybersecurity",
        "tagline": "Protect your systems, data, and reputation",
        "order": 4,
        "icon_svg": "25.svg",
        "image": "bjp-cybersecurity.webp",
        "description": (
            "Security is not optional — it is foundational. We apply enterprise-grade security "
            "practices to every engagement: web application firewalls, vulnerability assessments, "
            "penetration testing, and server hardening. When an incident occurs, our team responds "
            "fast — detecting, removing, and recovering from threats before they cause lasting damage."
        ),
        "bullet_points": (
            "Web Application & Server Security Hardening\n"
            "Web Application Firewall (WAF — ModSecurity)\n"
            "Vulnerability Assessment & Penetration Testing (VAPT)\n"
            "Malware Detection, Removal & Recovery\n"
            "Secure Authentication & Access Control"
        ),
    },
    {
        "name": "Managed IT Services",
        "slug": "managed-it-services",
        "tagline": "Your IT department — without the overhead",
        "order": 5,
        "icon_svg": "26.svg",
        "image": "bjp-managed-it-services.webp",
        "description": (
            "Running IT in-house is expensive and distracting. Our managed IT service gives you "
            "a dedicated team that monitors your infrastructure around the clock, handles routine "
            "maintenance and security patching, and is available when you need support. "
            "We proactively catch problems before they become outages — so your team stays focused "
            "on the business."
        ),
        "bullet_points": (
            "24/7 Server & Infrastructure Monitoring\n"
            "Routine Maintenance & Security Patching\n"
            "Application Support & Optimisation\n"
            "Data Backup & Recovery Management\n"
            "Remote IT Helpdesk Support"
        ),
    },
    {
        "name": "Payment & System Integrations",
        "slug": "payment-system-integrations",
        "tagline": "Connect your software to Tanzania's payment ecosystem",
        "order": 6,
        "icon_svg": "27.svg",
        "image": "bjp-payment-system-integrations.webp",
        "description": (
            "Tanzania's digital economy runs on mobile money. We integrate M-Pesa, Tigo Pesa, "
            "and Airtel Money natively into your software — not as an afterthought. We also connect "
            "bank payment gateways, Mastercard, Visa, and government APIs, giving your customers "
            "every payment option they expect and your business every transaction record you need."
        ),
        "bullet_points": (
            "Mobile Money Integration — M-Pesa, Tigo Pesa, Airtel Money\n"
            "Bank & Payment Gateway Integration\n"
            "Mastercard & Visa Integration\n"
            "Government & Third-Party API Integrations"
        ),
    },
    {
        "name": "IT Consulting & Advisory",
        "slug": "it-consulting-advisory",
        "tagline": "Strategic technology guidance for growing organisations",
        "order": 7,
        "icon_svg": "28.svg",
        "image": "bjp-it-consulting-advisory.webp",
        "description": (
            "Technology decisions made today shape your business for years. Our consulting "
            "team works alongside your leadership to design infrastructure that scales, plan "
            "cloud migrations that reduce cost, and build cybersecurity postures that satisfy "
            "compliance requirements. We translate technical complexity into clear business "
            "decisions — so you invest in the right things."
        ),
        "bullet_points": (
            "IT Infrastructure Design & Planning\n"
            "Cloud Migration & Optimisation\n"
            "Cybersecurity & Compliance Advisory\n"
            "Digital Transformation Strategy"
        ),
    },
]

INDUSTRIES = [
    {
        "name": "Startups & SMEs",
        "slug": "startups-smes",
        "tagline": "Affordable, scalable IT that grows with you",
        "order": 1,
        "image": "bjp-startups-smes.webp",
        "description": (
            "Early-stage companies and SMEs need technology that delivers results without "
            "enterprise price tags. We build the systems, websites, and infrastructure that "
            "help you launch fast, operate efficiently, and scale when the time comes — "
            "all with a local team that understands the Tanzanian market."
        ),
        "services_offered": (
            "Custom web applications and business systems\n"
            "Corporate website design and development\n"
            "Cloud infrastructure setup on DigitalOcean or AWS\n"
            "Mobile money payment integrations (M-Pesa, Tigo Pesa)\n"
            "IT consulting to plan your technology roadmap\n"
            "Managed IT support as your business grows"
        ),
    },
    {
        "name": "Financial Institutions",
        "slug": "financial-institutions",
        "tagline": "Secure, compliant systems for SACCOS and microfinance",
        "order": 2,
        "image": "bjp-financial-institutions.webp",
        "description": (
            "SACCOS, microfinance institutions, and banks operate in a high-stakes environment "
            "where security, accuracy, and compliance are non-negotiable. We build and maintain "
            "the loan management systems, payment integrations, and secure infrastructure that "
            "financial organisations depend on — with the reliability their members expect."
        ),
        "services_offered": (
            "SACCOS loan management and financial systems\n"
            "Mobile money and bank payment gateway integrations\n"
            "Cybersecurity hardening and VAPT assessments\n"
            "Secure authentication and access control\n"
            "24/7 server monitoring and incident response\n"
            "Compliance-focused IT advisory"
        ),
    },
    {
        "name": "NGOs & Development Organisations",
        "slug": "ngos-development",
        "tagline": "Technology that amplifies your mission",
        "order": 3,
        "image": "bjp-ngos-development.webp",
        "description": (
            "NGOs and development organisations need reliable, cost-effective technology that "
            "lets them focus on impact rather than IT problems. We deliver websites, data "
            "systems, and cloud infrastructure that keep your programmes running — and your "
            "donor reporting accurate."
        ),
        "services_offered": (
            "Institutional and programme websites\n"
            "Beneficiary data and reporting systems\n"
            "Cloud infrastructure setup and management\n"
            "Secure remote access and collaboration tools\n"
            "IT consulting for digital transformation\n"
            "Ongoing managed IT support"
        ),
    },
    {
        "name": "Education Institutions",
        "slug": "education",
        "tagline": "Digital tools for modern learning environments",
        "order": 4,
        "image": "bjp-education.webp",
        "description": (
            "Schools, colleges, and training institutions need technology that works reliably "
            "for students, staff, and administrators alike. We build student management systems, "
            "institutional websites, and the secure infrastructure that keeps academic data safe "
            "and accessible."
        ),
        "services_offered": (
            "Student management and academic systems\n"
            "Institutional websites and online portals\n"
            "Cloud-based data storage and backup\n"
            "Network infrastructure setup and management\n"
            "Cybersecurity awareness and endpoint protection\n"
            "IT helpdesk and managed support"
        ),
    },
    {
        "name": "Healthcare Providers",
        "slug": "healthcare",
        "tagline": "Reliable IT for patient-centred organisations",
        "order": 5,
        "image": "bjp-healthcare.webp",
        "description": (
            "Healthcare organisations handle sensitive patient data that demands the highest "
            "levels of security and reliability. We build and maintain the systems, secure "
            "infrastructure, and data management solutions that healthcare providers need — "
            "with the uptime their patients depend on."
        ),
        "services_offered": (
            "Patient management and health record systems\n"
            "Secure data storage and backup solutions\n"
            "Cybersecurity hardening and access control\n"
            "24/7 infrastructure monitoring\n"
            "Cloud migration for healthcare applications\n"
            "IT consulting for compliance and data protection"
        ),
    },
    {
        "name": "Retail & Wholesale Businesses",
        "slug": "retail-wholesale",
        "tagline": "Inventory, sales, and payments — all connected",
        "order": 6,
        "image": "bjp-retail-wholesale.webp",
        "description": (
            "Retail and wholesale businesses need fast, reliable systems at the point of sale "
            "and across the supply chain. We build the inventory management, POS, and e-commerce "
            "platforms that keep your operations running — and connect them to Tanzania's mobile "
            "money ecosystem so your customers can pay how they prefer."
        ),
        "services_offered": (
            "POS and inventory management systems\n"
            "E-commerce platform development\n"
            "Mobile money payment integrations\n"
            "Business website and online catalogue\n"
            "Cloud infrastructure for multi-branch operations\n"
            "Managed IT support and system maintenance"
        ),
    },
]


class Command(BaseCommand):
    help = "Seed Services and Industries with BJP Technologies content. Safe to re-run."

    def handle(self, *args, **kwargs) -> None:
        self._seed_services()
        self._seed_industries()

    def _seed_services(self) -> None:
        created = updated = 0
        for data in SERVICES:
            obj, is_new = Service.objects.update_or_create(
                slug=data["slug"],
                defaults={k: v for k, v in data.items() if k != "slug"},
            )
            if is_new:
                created += 1
            else:
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"Services — {created} created, {updated} updated"))

    def _seed_industries(self) -> None:
        created = updated = 0
        for data in INDUSTRIES:
            obj, is_new = Industry.objects.update_or_create(
                slug=data["slug"],
                defaults={k: v for k, v in data.items() if k != "slug"},
            )
            if is_new:
                created += 1
            else:
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"Industries — {created} created, {updated} updated"))
