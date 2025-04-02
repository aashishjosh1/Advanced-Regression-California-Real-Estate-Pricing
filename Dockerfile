FROM continuumio/anaconda3:2021.05
EXPOSE 8000
RUN apt-get update && \
    apt-get install -y apache2 \
    apache2-dev \
    vim \
 && apt-get clean \
 && apt-get autoremove \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /var/www/analysis_and_prediction_of_house_prices/
COPY ./ /var/www/analysis_and_prediction_of_house_prices/
RUN pip install -r requirements.txt
RUN /opt/conda/bin/mod_wsgi-express install-module
RUN mod_wsgi-express setup-server "/var/www/analysis_and_prediction_of_house_prices/source_code/analysis_and_prediction_of_house_prices.wsgi" --port=8000 \
    --user www-data --group www-data \
    --server-root=/etc/mod_wsgi-express-80
CMD ["/etc/mod_wsgi-express-80/apachectl", "start", "-D", "FOREGROUND"]