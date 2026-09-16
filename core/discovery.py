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
