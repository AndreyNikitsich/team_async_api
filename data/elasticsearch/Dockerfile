FROM elasticsearch:8.12.0 as data_builder
USER root
COPY indexes /data_builder/indexes
COPY create_indices.sh /data_builder/
RUN curl https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh > /data_builder/wait-for-it.sh \
    && chmod +x /data_builder/wait-for-it.sh \
    && mkdir -p /data_builder/result  \
    && chown -R elasticsearch:elasticsearch /data_builder
RUN echo "path.data: /data_builder/result" >> config/elasticsearch.yml \
    && echo "discovery.type: single-node" >> config/elasticsearch.yml \
    && echo "xpack.security.enabled: false" >> config/elasticsearch.yml
USER elasticsearch
RUN /usr/local/bin/docker-entrypoint.sh elasticsearch -p /tmp/epid -E path.data=/data_builder/result \
    & /bin/bash /data_builder/wait-for-it.sh -t 0 localhost:9200 -- \
    /data_builder/create_indices.sh;  kill $(cat /tmp/epid) \
    && wait $(cat /tmp/epid); exit 0; \
CMD [""]

FROM elasticsearch:8.12.0
COPY --from=data_builder /data_builder/result /usr/share/elasticsearch/data/
RUN echo "discovery.type: single-node" >> config/elasticsearch.yml \
    && echo "xpack.security.enabled: false" >> config/elasticsearch.yml
