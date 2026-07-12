import os
import pickle
from googleapiclient.discovery import build
from datetime import datetime, timedelta

def main():
    scratch_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(scratch_dir)
    token_path = os.path.join(root_dir, 'token.json')
    
    if not os.path.exists(token_path):
        print("Error: token.json not found! Please run test_gsc.py first.")
        return
        
    with open(token_path, 'rb') as token:
        creds = pickle.load(token)
        
    service = build('searchconsole', 'v1', credentials=creds)
    site_url = 'https://www.treeservicepocatelloidaho.com/'
    
    # Calculate date range (last 30 days)
    today = datetime.now()
    end_date = (today - timedelta(days=3)).strftime('%Y-%m-%d') # GSC data usually has a 3-day lag
    start_date = (today - timedelta(days=33)).strftime('%Y-%m-%d')
    
    print(f"Querying GSC data from {start_date} to {end_date} (US Only) for {site_url}...\n")
    
    # Country Filter (United States)
    country_filter = {
        'dimensionFilterGroups': [{
            'filters': [{
                'dimension': 'country',
                'operator': 'equals',
                'expression': 'usa'
            }]
        }]
    }
    
    # 1. Global Performance Metrics
    try:
        global_request = {
            'startDate': start_date,
            'endDate': end_date,
            **country_filter
        }
        global_response = service.searchanalytics().query(siteUrl=site_url, body=global_request).execute()
        
        # Calculate totals
        total_clicks = 0
        total_impressions = 0
        sum_position = 0
        row_count = 0
        
        # We need to query with dimensions to get actual query totals or use the simple response
        if 'rows' in global_response:
            for row in global_response['rows']:
                total_clicks += row.get('clicks', 0)
                total_impressions += row.get('impressions', 0)
                sum_position += row.get('position', 0) * row.get('impressions', 0)
                row_count += 1
        
        print("=== GLOBAL PERFORMANCE (LAST 30 DAYS - US ONLY) ===")
        # Request without dimensions gives overall totals
        summary_request = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': [],
            **country_filter
        }
        summary_res = service.searchanalytics().query(siteUrl=site_url, body=summary_request).execute()
        if 'rows' in summary_res and len(summary_res['rows']) > 0:
            row = summary_res['rows'][0]
            print(f"Total Clicks: {row.get('clicks', 0)}")
            print(f"Total Impressions: {row.get('impressions', 0):,}")
            print(f"Average CTR: {row.get('ctr', 0)*100:.2f}%")
            print(f"Average Position: {row.get('position', 0):.1f}")
        print("=========================================\n")
        
    except Exception as e:
        print(f"Error fetching global performance: {e}")

    # 2. Striking Distance Keywords (Position 11 - 25, sorted by impressions)
    try:
        query_request = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': ['query'],
            'rowLimit': 1000,
            **country_filter
        }
        query_response = service.searchanalytics().query(siteUrl=site_url, body=query_request).execute()
        
        striking_distance = []
        if 'rows' in query_response:
            for row in query_response['rows']:
                query = row['keys'][0]
                clicks = row.get('clicks', 0)
                impressions = row.get('impressions', 0)
                ctr = row.get('ctr', 0)
                position = row.get('position', 0)
                
                # Striking distance = Page 2 / top of Page 3 (10.5 to 25)
                if 10.5 <= position <= 25.0:
                    striking_distance.append({
                        'query': query,
                        'clicks': clicks,
                        'impressions': impressions,
                        'ctr': ctr * 100,
                        'position': position
                    })
                    
        # Sort by impressions descending
        striking_distance = sorted(striking_distance, key=lambda x: x['impressions'], reverse=True)
        
        print("=== STRIKING DISTANCE OPPORTUNITIES (Page 2 Keywords) ===")
        print(f"{'Keyword':<40} | {'Impressions':<12} | {'Clicks':<8} | {'CTR':<6}% | {'Position':<8}")
        print("-" * 80)
        for item in striking_distance[:15]:
            print(f"{item['query']:<40} | {item['impressions']:<12,} | {item['clicks']:<8} | {item['ctr']:<6.2f}% | {item['position']:<8.1f}")
        print("=========================================================\n")
        
    except Exception as e:
        print(f"Error fetching queries: {e}")

    # 3. High Impressions, Low CTR Pages (CTR < 1%, Impressions > 100, sorted by impressions)
    try:
        page_request = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': ['page'],
            'rowLimit': 100,
            **country_filter
        }
        page_response = service.searchanalytics().query(siteUrl=site_url, body=page_request).execute()
        
        ctr_opportunities = []
        if 'rows' in page_response:
            for row in page_response['rows']:
                page = row['keys'][0]
                clicks = row.get('clicks', 0)
                impressions = row.get('impressions', 0)
                ctr = row.get('ctr', 0)
                position = row.get('position', 0)
                
                # High impressions but low CTR
                if ctr < 0.015 and impressions >= 50:
                    # Strip domain name for readability
                    display_page = page.replace(site_url, '/')
                    ctr_opportunities.append({
                        'page': display_page,
                        'clicks': clicks,
                        'impressions': impressions,
                        'ctr': ctr * 100,
                        'position': position
                    })
                    
        # Sort by impressions descending
        ctr_opportunities = sorted(ctr_opportunities, key=lambda x: x['impressions'], reverse=True)
        
        print("=== LOW CTR PAGES (Title/Meta Optimization Opportunities) ===")
        print(f"{'Page URL':<40} | {'Impressions':<12} | {'Clicks':<8} | {'CTR':<6}% | {'Position':<8}")
        print("-" * 80)
        for item in ctr_opportunities[:15]:
            print(f"{item['page']:<40} | {item['impressions']:<12,} | {item['clicks']:<8} | {item['ctr']:<6.2f}% | {item['position']:<8.1f}")
        print("=============================================================\n")
        
    except Exception as e:
        print(f"Error fetching pages: {e}")

if __name__ == '__main__':
    main()
