# ideal of this task, we'll count number line of slow query log file of yesterday and today, After that get the sub of $a =  (today - yesterday) 
# tail -n $a slow_query_log.log to get log of today
# This is script 

#!/bin/bash			
DATE=`date +%Y-%m-%d`			
DIR=/opt/scripts/databases/logs/
NUM_LINE=/opt/scripts/databases/num_line_yesterday			
FILE_LOG=/opt/mysql/data/tft-dbslave1-slow.log			
cd $DIR			
current_line=`wc -l /opt/mysql/data/tft-dbslave1-slow.log | awk '{print $1}'`			
yesterday_line=`cat $NUM_LINE`			
num=`expr $current_line - $yesterday_line`			
#echo $num			
tail -n $num $FILE_LOG > $DIR/slow_query_slave_trsbase_$DATE			
echo $current_line > $NUM_LINE			
scp -i /root/.ssh/id_rsa_tfx $DIR/slow_query_slave_trsbase_$DATE $IP:/tmp/slow_query/slow_log



# this script put crontab to do get slow query from remote server
#!/bin/bash

DATE=`date +%Y-%m-%d`
#cat /dev/null > $DATE.txt
#for ip in `cat /opt/script/databases/ip_server.txt`
#do
#echo "---- $ip -----"  >> /opt/script/databases/logs/$DATE.txt
#ssh $ip "sh /opt/scripts/databases/checklog_slow.sh" >>  /opt/script/databases/logs/$DATE.txt
#echo "-------- -----"  >> /opt/script/databases/logs/$DATE.txt
#done
ssh -i /opt/script/databases/id_rsa_trsbase_slave root@10.8.20.47 "sh /opt/scripts/databases/checklog_slow.sh"
sleep 20

ssh -i /opt/script/databases/id_rsa_trsbase_master root@10.8.20.40 "sh /opt/scripts/databases/checklog_slow.sh"
sleep 20

ssh -i /opt/script/databases/id_rsa_report root@10.8.20.30 "sh /opt/scripts/databases/checklog_slow.sh"
sleep 25

ssh -i /opt/script/databases/id_rsa_trsbo root@10.8.21.121 "sh /opt/scripts/databases/checklog_slow.sh"
sleep 20

cd /tmp/slow_query/ && tar -zcvf slow_log.tar.gz slow_log/*$DATE* && rm -rf slow_log/*$DATE*

echo "Please refer to the attachment below for check slow query log database $DATE" | mutt  tung.nguyen.thanh@nextop.asia thang.tran.dai@nextop.asia quyen.le.manh@nextop.asia ops-vn@nextop.asia -a "/tmp/slow_query/slow_log.tar.gz" -s "[TRS][PRO] Slow query for database $DATE"
