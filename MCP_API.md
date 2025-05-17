# MCP API Documentation

This document describes the MCP tool interface for all Venture Insights agents. For each MCP tool, the tool name, argument schema, and a sample MCP request JSON are provided.

---

## Finance Agent

### Tool: `revenue_analysis`
**Arguments:**
- `company_name` (str, required)
- `domain` (str, optional)
- `start_date` (str, optional, format: YYYY-MM-DD)
- `end_date` (str, optional, format: YYYY-MM-DD)
- `granularity` (str, optional, default: "year")

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "revenue_analysis",
  "params": {
    "company_name": "TechNova Inc.",
    "domain": "technova.com",
    "start_date": "2023-01-01",
    "end_date": "2023-12-31",
    "granularity": "quarter"
  },
  "id": 1
}
```

### Tool: `expense_analysis`
**Arguments:**
- `company_name` (str, required)
- `domain` (str, optional)
- `year` (int, optional)
- `category` (str, optional)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "expense_analysis",
  "params": {
    "company_name": "TechNova Inc.",
    "domain": "technova.com",
    "year": 2023,
    "category": "R&D"
  },
  "id": 1
}
```

### Tool: `profit_margins`
**Arguments:**
- `company_name` (str, required)
- `domain` (str, optional)
- `year` (int, optional)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "profit_margins",
  "params": {
    "company_name": "TechNova Inc.",
    "domain": "technova.com",
    "year": 2023
  },
  "id": 1
}
```

### Tool: `valuation_estimation`
**Arguments:**
- `company_name` (str, required)
- `domain` (str, optional)
- `as_of_date` (str, optional, format: YYYY-MM-DD)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "valuation_estimation",
  "params": {
    "company_name": "TechNova Inc.",
    "domain": "technova.com",
    "as_of_date": "2024-05-01"
  },
  "id": 1
}
```

### Tool: `funding_history`
**Arguments:**
- `company_name` (str, required)
- `domain` (str, optional)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "funding_history",
  "params": {
    "company_name": "TechNova Inc.",
    "domain": "technova.com"
  },
  "id": 1
}
```

---

## LinkedIn Team Agent

### Tool: `team_overview`
**Arguments:**
- `company_name` (str, required)
- `domain` (str, optional)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "team_overview",
  "params": {
    "company_name": "TechNova Inc.",
    "domain": "technova.com"
  },
  "id": 1
}
```

### Tool: `individual_performance`
**Arguments:**
- `company_name` (str, required)
- `domain` (str, optional)
- `individual_name` (str, required)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "individual_performance",
  "params": {
    "company_name": "TechNova Inc.",
    "domain": "technova.com",
    "individual_name": "Jane Doe"
  },
  "id": 1
}
```

### Tool: `org_structure`
**Arguments:**
- `company_name` (str, required)
- `domain` (str, optional)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "org_structure",
  "params": {
    "company_name": "TechNova Inc.",
    "domain": "technova.com"
  },
  "id": 1
}
```

### Tool: `team_growth`
**Arguments:**
- `company_name` (str, required)
- `domain` (str, optional)
- `start_date` (str, optional, format: YYYY-MM-DD)
- `end_date` (str, optional, format: YYYY-MM-DD)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "team_growth",
  "params": {
    "company_name": "TechNova Inc.",
    "domain": "technova.com",
    "start_date": "2023-01-01",
    "end_date": "2023-12-31"
  },
  "id": 1
}
```

---

## Market Analysis Agent

### Tool: `market_trends`
**Arguments:**
- `industry` (str, required)
- `region` (str, optional)
- `start_date` (str, optional, format: YYYY-MM-DD)
- `end_date` (str, optional, format: YYYY-MM-DD)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "market_trends",
  "params": {
    "industry": "FinTech",
    "region": "North America",
    "start_date": "2023-01-01",
    "end_date": "2023-12-31"
  },
  "id": 1
}
```

### Tool: `competitive_analysis`
**Arguments:**
- `company_name` (str, required)
- `domain` (str, optional)
- `industry` (str, optional)
- `region` (str, optional)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "competitive_analysis",
  "params": {
    "company_name": "TechNova Inc.",
    "domain": "technova.com",
    "industry": "FinTech",
    "region": "North America"
  },
  "id": 1
}
```

### Tool: `growth_projections`
**Arguments:**
- `industry` (str, required)
- `region` (str, optional)
- `start_date` (str, optional, format: YYYY-MM-DD)
- `end_date` (str, optional, format: YYYY-MM-DD)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "growth_projections",
  "params": {
    "industry": "FinTech",
    "region": "North America",
    "start_date": "2023-01-01",
    "end_date": "2023-12-31"
  },
  "id": 1
}
```

### Tool: `regional_trends`
**Arguments:**
- `industry` (str, required)
- `regions` (list of str, optional)
- `start_date` (str, optional, format: YYYY-MM-DD)
- `end_date` (str, optional, format: YYYY-MM-DD)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "regional_trends",
  "params": {
    "industry": "FinTech",
    "regions": ["North America", "Europe"],
    "start_date": "2023-01-01",
    "end_date": "2023-12-31"
  },
  "id": 1
}
```

---

## Risk Analysis Agent

### Tool: `regulatory_risks`
**Arguments:**
- `company_name` (str, required)
- `domain` (str, optional)
- `industry` (str, optional)
- `region` (str, optional)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "regulatory_risks",
  "params": {
    "company_name": "TechNova Inc.",
    "domain": "technova.com",
    "industry": "FinTech",
    "region": "Europe"
  },
  "id": 1
}
```

### Tool: `market_risks`
**Arguments:**
- `company_name` (str, required)
- `domain` (str, optional)
- `industry` (str, optional)
- `region` (str, optional)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "market_risks",
  "params": {
    "company_name": "TechNova Inc.",
    "domain": "technova.com",
    "industry": "FinTech",
    "region": "Europe"
  },
  "id": 1
}
```

### Tool: `operational_risks`
**Arguments:**
- `company_name` (str, required)
- `domain` (str, optional)
- `industry` (str, optional)
- `region` (str, optional)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "operational_risks",
  "params": {
    "company_name": "TechNova Inc.",
    "domain": "technova.com",
    "industry": "FinTech",
    "region": "Europe"
  },
  "id": 1
}
```

### Tool: `legal_risks`
**Arguments:**
- `company_name` (str, required)
- `domain` (str, optional)
- `industry` (str, optional)
- `region` (str, optional)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "legal_risks",
  "params": {
    "company_name": "TechNova Inc.",
    "domain": "technova.com",
    "industry": "FinTech",
    "region": "Europe"
  },
  "id": 1
}
```

---

## Customer Sentiment Agent

### Tool: `sentiment_summary`
**Arguments:**
- `company_name` (str, required)
- `domain` (str, optional)
- `product` (str, optional)
- `region` (str, optional)
- `start_date` (str, optional, format: YYYY-MM-DD)
- `end_date` (str, optional, format: YYYY-MM-DD)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "sentiment_summary",
  "params": {
    "company_name": "TechNova Inc.",
    "domain": "technova.com",
    "product": "NovaPay",
    "region": "Europe",
    "start_date": "2023-01-01",
    "end_date": "2023-12-31"
  },
  "id": 1
}
```

### Tool: `customer_feedback`
**Arguments:**
- `company_name` (str, required)
- `domain` (str, optional)
- `product` (str, optional)
- `region` (str, optional)
- `start_date` (str, optional, format: YYYY-MM-DD)
- `end_date` (str, optional, format: YYYY-MM-DD)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "customer_feedback",
  "params": {
    "company_name": "TechNova Inc.",
    "domain": "technova.com",
    "product": "NovaPay",
    "region": "Europe",
    "start_date": "2023-01-01",
    "end_date": "2023-12-31"
  },
  "id": 1
}
```

### Tool: `brand_reputation`
**Arguments:**
- `company_name` (str, required)
- `domain` (str, optional)
- `region` (str, optional)
- `start_date` (str, optional, format: YYYY-MM-DD)
- `end_date` (str, optional, format: YYYY-MM-DD)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "brand_reputation",
  "params": {
    "company_name": "TechNova Inc.",
    "domain": "technova.com",
    "region": "Europe",
    "start_date": "2023-01-01",
    "end_date": "2023-12-31"
  },
  "id": 1
}
```

---

## Regulatory Compliance Agent

### Tool: `compliance_overview`
**Arguments:**
- `company_name` (str, required)
- `domain` (str, optional)
- `industry` (str, optional)
- `region` (str, optional)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "compliance_overview",
  "params": {
    "company_name": "TechNova Inc.",
    "domain": "technova.com",
    "industry": "FinTech",
    "region": "Europe"
  },
  "id": 1
}
```

### Tool: `violation_history`
**Arguments:**
- `company_name` (str, required)
- `domain` (str, optional)
- `industry` (str, optional)
- `region` (str, optional)
- `start_date` (str, optional, format: YYYY-MM-DD)
- `end_date` (str, optional, format: YYYY-MM-DD)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "violation_history",
  "params": {
    "company_name": "TechNova Inc.",
    "domain": "technova.com",
    "industry": "FinTech",
    "region": "Europe",
    "start_date": "2023-01-01",
    "end_date": "2023-12-31"
  },
  "id": 1
}
```

### Tool: `compliance_risk`
**Arguments:**
- `company_name` (str, required)
- `domain` (str, optional)
- `industry` (str, optional)
- `region` (str, optional)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "compliance_risk",
  "params": {
    "company_name": "TechNova Inc.",
    "domain": "technova.com",
    "industry": "FinTech",
    "region": "Europe"
  },
  "id": 1
}
```

### Tool: `regional_compliance`
**Arguments:**
- `company_name` (str, required)
- `domain` (str, optional)
- `industry` (str, optional)
- `regions` (list of str, optional)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "regional_compliance",
  "params": {
    "company_name": "TechNova Inc.",
    "domain": "technova.com",
    "industry": "FinTech",
    "regions": ["Europe", "Asia"]
  },
  "id": 1
}
```

---

## Partnership Network Agent

### Tool: `partner_list`
**Arguments:**
- `company_name` (str, required)
- `domain` (str, optional)
- `industry` (str, optional)
- `region` (str, optional)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "partner_list",
  "params": {
    "company_name": "TechNova Inc.",
    "domain": "technova.com",
    "industry": "FinTech",
    "region": "Europe"
  },
  "id": 1
}
```

### Tool: `strategic_alliances`
**Arguments:**
- `company_name` (str, required)
- `domain` (str, optional)
- `industry` (str, optional)
- `region` (str, optional)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "strategic_alliances",
  "params": {
    "company_name": "TechNova Inc.",
    "domain": "technova.com",
    "industry": "FinTech",
    "region": "Europe"
  },
  "id": 1
}
```

### Tool: `network_strength`
**Arguments:**
- `company_name` (str, required)
- `domain` (str, optional)
- `industry` (str, optional)
- `region` (str, optional)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "network_strength",
  "params": {
    "company_name": "TechNova Inc.",
    "domain": "technova.com",
    "industry": "FinTech",
    "region": "Europe"
  },
  "id": 1
}
```

### Tool: `partnership_trends`
**Arguments:**
- `company_name` (str, required)
- `domain` (str, optional)
- `industry` (str, optional)
- `region` (str, optional)
- `start_date` (str, optional, format: YYYY-MM-DD)
- `end_date` (str, optional, format: YYYY-MM-DD)

**Sample MCP Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "partnership_trends",
  "params": {
    "company_name": "TechNova Inc.",
    "domain": "technova.com",
    "industry": "FinTech",
    "region": "Europe",
    "start_date": "2023-01-01",
    "end_date": "2023-12-31"
  },
  "id": 1
}
``` 