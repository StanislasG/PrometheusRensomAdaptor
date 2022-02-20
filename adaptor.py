from prometheus_client import start_http_server, Summary, Gauge
import time
import requests


# labels = ['CO2',
#  'ETA constant flow sensor value',
#  'ETA fan speed',
#  'Measured ETA airflow',
#  'Measured SUP airflow',
#  'SUP constant flow sensor value',
#  'SUP fan speed']

g = Gauge('customapp_activedevices', 'Description of gauge', labelnames=['parameter'])
url='CHANGE HERE'

if __name__ == '__main__':
    start_http_server(9000)
    next_wsn = 0
    init = True
    while True:
        curr_wsn = next_wsn
        r = requests.get(url+'/JSON/ModifiedItems?wsn='+str(curr_wsn))
        data = r.json()
        next_wsn = data['Wsn']

        if(init != True):
            try:
                for j in range(len(data['ModifiedItems'])):
                    # print(data['ModifiedItems'][j])
                    name = data['ModifiedItems'][j]['Name']
                    value = data['ModifiedItems'][j]['Value']
                    g.labels(parameter = name).set(value)

                time.sleep(next_wsn - curr_wsn)
            except Exception:
                pass
        else:
            init=False