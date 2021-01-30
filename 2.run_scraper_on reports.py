import os 
from scrape_partial_report import scrape_partial_report
from scrape_report_detail import scrape_report_detail 

def run_reports_scraper():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    html_input_dir = os.path.join(dir_path, 'input_html')
    json_output_dir = os.path.join(dir_path, 'output_json')
    
    for root, d_names, f_names in os.walk(html_input_dir):
        for list_fname in f_names:
            if list_fname.endswith('.html') and 'Detail' in list_fname:
                try: 
                    scrape_report_detail(html_input_dir, json_output_dir, list_fname)
                except AttributeError as e:
                    print ('File ' + list_fname + 'caused following error: ' + e)
            elif list_fname.endswith('.html') and 'Zpráva k projektu' in list_fname:
                try:
                    scrape_partial_report(html_input_dir, json_output_dir, list_fname)
                except AttributeError as e:
                    print ('File {} caused following error: {}'.format(list_fname, e))
            else:
                pass

    return

if __name__ == '__main__':
    run_reports_scraper()
