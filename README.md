# Idaho Representatives Contact Tool

A Python tool to help Idaho residents contact their state representatives and navigate the legislative process.

## Features

- **Find Your Representatives**: Look up your state senator and house representatives by district
- **Committee Information**: See which committees each representative serves on
- **Problem Analysis**: Get recommendations on which committees and representatives to contact for specific issues
- **Representative Research**: Deep analysis of individual representatives including their interests, background, and political risk assessment

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Find Representatives by District
```bash
python main.py --district 15
```

### Analyze a Problem
```bash
python main.py --problem "Need better funding for rural schools"
```

### Research a Specific Representative
```bash
python main.py --analyze "Brad Little"
```

### List All Committees
```bash
python main.py --committees
```

## Examples

**Finding your representatives:**
```bash
$ python main.py --district 5
REPRESENTATIVES FOR DISTRICT 5

Senator: John Doe (R)
Email: jdoe@gov.idaho.gov
Phone: (208) 332-1000

House Representatives:
  Jane Smith (R) - Seat A
  Email: jsmith@gov.idaho.gov
  Phone: (208) 332-1001
```

**Problem analysis:**
```bash
$ python main.py --problem "Small businesses need tax relief"
PROBLEM ANALYSIS
Problem: Small businesses need tax relief

Recommended Committees:
  - Revenue & Taxation
  - Commerce & Human Resources

Target Representatives:
  - John Doe (District 5, Senate)
  - Jane Smith (District 5, House)

Strategy: Target the Revenue & Taxation and Commerce & Human Resources committees...
```

## Data Sources

This tool scrapes data from the official Idaho Legislature website (https://legislature.idaho.gov/) to ensure accuracy and up-to-date information.

## Note

For enhanced representative analysis features, you can optionally provide an OpenAI API key to enable more detailed political analysis.