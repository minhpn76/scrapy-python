from crontab import CronTab

cron = CronTab()
job = cron.new(command='scrapy crawl cronjob')
job.hour.every(4)

cron.write()