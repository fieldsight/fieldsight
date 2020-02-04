FROM fieldsightdocker/fieldsight_web:latest

RUN apt-get update --fix-missing && \
  apt-get upgrade -y -o Dpkg::Options::="--force-confold" && \
  apt-get install -y --no-install-recommends cron && \
  apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy fieldsight-cron file to the cron.d directory
COPY fieldsight_corn /etc/cron.d/fieldsight_corn

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/fieldsight_corn

# Apply cron job
RUN crontab /etc/cron.d/fieldsight_corn

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

CMD ["cron", "-f"]
