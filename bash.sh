#!/bin/bash

rm /home/sauravtom/public_html/coupon-log.txt
touch /home/sauravtom/public_html/coupon-log.txt

if [ -n "${FROMCRON}" ]
then
	echo "Run mode : CRON" >> /home/sauravtom/public_html/coupon-log.txt
else
	echo "Run mode : MANUAL" >> /home/sauravtom/public_html/coupon-log.txt
fi
DATE=$( TZ='Asia/Kolkata' date  +DATE:%F\ TIME:%T\(IST\) )
echo "Start $DATE" >> /home/sauravtom/public_html/coupon-log.txt
python /home/sauravtom/coupon/scra.py >> /home/sauravtom/public_html/coupon-log.txt
DATE=$( TZ='Asia/Kolkata' date  +DATE:%F\ TIME:%T\(IST\) )
echo "End $DATE" >> /home/sauravtom/public_html/coupon-log.txt
