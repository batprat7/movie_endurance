from pytrends.request import TrendReq

print('pytrends imported')

from datetime import datetime as dt

# tf = 'today 5-y'

def parseDateTime(datetime, dt_format='%Y-%m-%d'):
	d = dt.strptime(datetime, dt_format)
	return {
		'year': d.date().year,
		'month': d.date().month,
		'day': d.date().day,
		'hour': d.time().hour,
		'minute': d.time().minute,
		'second': d.time().second
		}

def getTrends(movieList, start, end):
	s = parseDateTime(start)
	e = parseDateTime(end)

	pt = TrendReq(hl='en-US', tz=360, timeout=(10,25), retries=2, backoff_factor=0.1)
	return pt.get_historical_interest(
		movieList,
		year_start=s['year'],
		month_start=s['month'],
		day_start=s['day'],
		hour_start=s['hour'],
		year_end=e['year'],
		month_end=e['month'],
		day_end=e['day'],
		hour_end=e['hour'],
		cat=0,
		geo='',
		gprop='',
		sleep=0
	)

print(getTrends(['The Dark Knight'], '2018-01-01', '2019-11-10'))