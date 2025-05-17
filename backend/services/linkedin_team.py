from datetime import datetime


class LinkedInTeamService:
    def __init__(self):
        pass

    async def get_team_overview(self):
        return {
            "company_name": "TechNova Inc.",
            "total_employees": 120,
            "roles_breakdown": [
                {
                    "role": "Engineering",
                    "count": 60,
                    "sources": ["https://linkedin.com/company/tecnova"],
                    "confidence": 0.95,
                },
                {
                    "role": "Product",
                    "count": 20,
                    "sources": ["https://linkedin.com/company/tecnova"],
                    "confidence": 0.9,
                },
                {
                    "role": "Sales",
                    "count": 15,
                    "sources": ["https://linkedin.com/company/tecnova"],
                    "confidence": 0.85,
                },
                {
                    "role": "Marketing",
                    "count": 10,
                    "sources": ["https://linkedin.com/company/tecnova"],
                    "confidence": 0.8,
                },
                {
                    "role": "Leadership",
                    "count": 5,
                    "sources": ["https://linkedin.com/company/tecnova"],
                    "confidence": 0.99,
                },
            ],
            "locations": ["San Francisco", "Remote"],
            "sources": ["https://linkedin.com/company/tecnova"],
            "last_updated": datetime.now().isoformat(),
        }

    async def get_individual_performance(self):
        return {
            "company_name": "TechNova Inc.",
            "individual_name": "Jane Doe",
            "title": "VP of Engineering",
            "tenure_years": 3.5,
            "performance_metrics": [
                {
                    "metric": "Endorsements",
                    "value": 120,
                    "sources": ["https://linkedin.com/in/janedoe"],
                    "confidence": 0.9,
                },
                {
                    "metric": "Connections",
                    "value": 800,
                    "sources": ["https://linkedin.com/in/janedoe"],
                    "confidence": 0.95,
                },
                {
                    "metric": "Articles Published",
                    "value": 5,
                    "sources": ["https://linkedin.com/in/janedoe"],
                    "confidence": 0.8,
                },
            ],
            "sources": ["https://linkedin.com/in/janedoe"],
            "last_updated": datetime.now().isoformat(),
        }

    async def get_org_structure(self):
        return {
            "company_name": "TechNova Inc.",
            "org_chart": [
                {
                    "name": "Jane Doe",
                    "title": "VP of Engineering",
                    "reports_to": "CEO",
                    "direct_reports": ["John Smith", "Alice Lee"],
                    "sources": ["https://linkedin.com/in/janedoe"],
                },
                {
                    "name": "John Smith",
                    "title": "Engineering Manager",
                    "reports_to": "Jane Doe",
                    "direct_reports": ["Bob Brown"],
                    "sources": ["https://linkedin.com/in/johnsmith"],
                },
                {
                    "name": "Alice Lee",
                    "title": "Engineering Manager",
                    "reports_to": "Jane Doe",
                    "direct_reports": [],
                    "sources": ["https://linkedin.com/in/alicelee"],
                },
                {
                    "name": "Bob Brown",
                    "title": "Software Engineer",
                    "reports_to": "John Smith",
                    "direct_reports": [],
                    "sources": ["https://linkedin.com/in/bobbrown"],
                },
            ],
            "sources": ["https://linkedin.com/company/tecnova"],
            "last_updated": datetime.now().isoformat(),
        }

    async def get_team_growth(self):
        return {
            "company_name": "TechNova Inc.",
            "team_growth_timeseries": [
                {
                    "period_start": "2023-01-01",
                    "period_end": "2023-03-31",
                    "hires": 10,
                    "attrition": 2,
                    "net_growth": 8,
                    "sources": ["https://linkedin.com/company/tecnova"],
                    "confidence": 0.9,
                },
                {
                    "period_start": "2023-04-01",
                    "period_end": "2023-06-30",
                    "hires": 7,
                    "attrition": 3,
                    "net_growth": 4,
                    "sources": ["https://linkedin.com/company/tecnova"],
                    "confidence": 0.85,
                },
            ],
            "total_hires": 17,
            "total_attrition": 5,
            "net_growth": 12,
            "sources": ["https://linkedin.com/company/tecnova"],
            "last_updated": datetime.now().isoformat(),
        }
