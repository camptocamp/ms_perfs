FROM denvazh/gatling:2.2.1

COPY run.sh /usr/bin/run.sh
COPY com /opt/gatling/user-files/simulations/com

ENTRYPOINT ["/bin/sh", "-c"]
CMD ["/usr/bin/run.sh"]
