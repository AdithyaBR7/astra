import whois
import csv

def get_whois_data(domain):
    try:
        w = whois.whois(domain)
        return {
            "Domain": domain,
            "Registrar": w.registrar,
            "Registrant Country": w.country if hasattr(w, 'country') else None,
            "Registrant Organization": w.org if hasattr(w, 'org') else None,
            "Creation Date": w.creation_date,
            "Expiration Date": w.expiration_date,
            "Name Servers": ", ".join(w.name_servers) if w.name_servers else None,
            "Status": w.status if isinstance(w.status, str) else ", ".join(w.status) if w.status else None,
            "Emails": ", ".join(w.emails) if w.emails else None
        }
    except Exception as e:
        print(f"Error fetching WHOIS data for {domain}: {e}")
        return None

def save_to_csv(data, filename="whois_data.csv"):
    if not data:
        print("No data to save.")
        return
    
    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"WHOIS data saved to {filename}")

def main():
    domains = ["amnic.com", "amnic.cn", "cybersecify.com"]  # Add your domains here
    whois_data = [get_whois_data(domain) for domain in domains if get_whois_data(domain)]
    save_to_csv(whois_data)

if __name__ == "__main__":
    main()
