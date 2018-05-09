# AWS Setup Guide

## Monitoring charges
- Use the AWS Lambda service to set up a new CloudWatch scheduled event that triggers daily.
- Use the python function provided in `resources/aws-lambda-watch.py`
- Make sure the alarm thresholds are as desired
- Optionally set up long-term monthly budget alarms using the CloudWatch built in system.

## Repository AMI Instances
- At the time of this writing these require at least ~10 GB of memory as that is the size of the _Nature_ data (7GB).
- Follow standard procedures for creating EC2 instances from an AMI for these instance types, and ssh in as normal. No other setup is required.

## Elasticsearch Node Instances
- You will need some storage space for the documents. Assign a security group that ONLY ALLOWS TRAFFIC FROM THE PROXY
- Depending on how much memory you allocate to the node you will need to change the heap size according to [https://www.elastic.co/guide/en/elasticsearch/reference/current/heap-size.html](https://www.elastic.co/guide/en/elasticsearch/reference/current/heap-size.html)
- Then restart the service using the systemd commands found at (https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html#deb-running-systemd)[https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html#deb-running-systemd]
- Modify the main config yml file found in `/etc/elasticsearch/` to reflect the PRIVATE URL of the node (found on the EC2 console)
- For multi-node clusters you need to change the main .yml settings file to specify the other nodes in the cluster.

## Elasticsearch Proxy Instances
- A `t2.micro` is generally fine for these instances. The security setting is not important as long as it is not too restrictive.
- Test that NGINX is working by navigating to the analyis page. If your instance was at `ec2-34-201-3-67.compute-1` this would be `http://ec2-34-201-3-67.compute-1.amazonaws.com/analysis/index.html`
- Modify the `conf.d/` contents to proxy traffic to your Elasticsearch cluster (just specify the public URL).
- You will need to `sudo nginx -s reload` after changing any of the NGINX settings.