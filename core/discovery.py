from datetime import datetime, timezone


def create_evidence(
    fact,
    source_name,
    source_url,
    evidence_type="public_web",
):
    """
    Create a traceable evidence record for B2B Bridge AI.

    Every factual claim used by the AI should be connected
    to a source whenever possible.
    """

    return {
        "fact": fact,
        "source_name": source_name,
        "source_url": source_url,
        "evidence_type": evidence_type,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
    }


def build_company_profile(
    name,
    country=None,
    industry=None,
    products=None,
    technologies=None,
    markets=None,
    needs=None,
    signals=None,
    evidence=None,
):
    """
    Build a standardized company profile for B2B analysis.
    """

    return {
        "name": name,
        "country": country,
        "industry": industry,
        "products": products or [],
        "technologies": technologies or [],
        "markets": markets or [],
        "needs": needs or [],
        "signals": signals or [],
        "evidence": evidence or [],
    }


def search_companies_gleif(name, country=None, limit=10):
    """
    Search real legal entities using the free GLEIF API.
    """

    import requests

    url = "https://" + "api.gleif.org/api/v1/lei-records"

    params = {
        "filter[entity.legalName]": name,
        "page[size]": limit,
    }

    if country:
        params["filter[entity.legalAddress.country]"] = country.upper()

    response = requests.get(
        url,
        params=params,
        timeout=20,
    )

    response.raise_for_status()

    data = response.json()

    companies = []

    for record in data.get("data", []):
        attributes = record["attributes"]
        entity = attributes["entity"]
        address = entity.get("legalAddress", {})

        companies.append(
            {
                "name": entity["legalName"]["name"],
                "city": address.get("city"),
                "region": address.get("region"),
                "country": address.get("country"),
                "postal_code": address.get("postalCode"),
                "address": address.get("addressLines", []),
                "lei": attributes["lei"],
                "registered_as": entity.get("registeredAs"),
                "registered_at": entity.get("registeredAt", {}).get("id"),
                "jurisdiction": entity.get("jurisdiction"),
                "category": entity.get("category"),
                "legal_form": entity.get("legalForm", {}).get("id"),
                "status": entity.get("status"),
                "creation_date": entity.get("creationDate"),
                "corporate_events": entity.get("eventGroups", []),
                "source": "GLEIF",
            }
        )

    return companies


def rank_company_candidates(companies, search_name):
    """
    Rank company candidates using objective identity signals.
    """

    search = search_name.strip().lower()

    def calculate_score(company):
        score = 0
        name = company.get("name", "").lower()

        # Prefer active entities.
        if company.get("status") == "ACTIVE":
            score += 10

        # Prefer operating/general entities over funds.
        if company.get("category") == "GENERAL":
            score += 30
        elif company.get("category") == "FUND":
            score -= 30

        # Name relevance.
        if name == search:
            score += 100
        elif name.startswith(search + " "):
            score += 50
        elif search in name:
            score += 20

        company["identity_score"] = score
        return score

    return sorted(
        companies,
        key=calculate_score,
        reverse=True,
    )


def get_legal_form(legal_form_code):
    """
    Resolve a GLEIF ELF code into a human-readable legal form.
    """

    import requests

    if not legal_form_code:
        return None

    url = (
        "https://api.gleif.org/api/v1/entity-legal-forms/"
        + legal_form_code
    )

    response = requests.get(url, timeout=20)
    response.raise_for_status()

    data = response.json()
    attributes = data["data"]["attributes"]
    names = attributes.get("names", [])

    if not names:
        return None

    return {
        "code": legal_form_code,
        "name": names[0].get("localName"),
        "country": attributes.get("country"),
        "country_code": attributes.get("countryCode"),
        "status": attributes.get("status"),
    }
