FROM node:20
WORKDIR /dashboard
RUN npm install express@^4.18.2
RUN npm install body-parser@^1.20.2
RUN npm install papaparse@^5.4.1
RUN npm install http@^0.0.1-security
RUN npm install socket.io@^4.7.2
COPY ./ /dashboard
EXPOSE 4400
CMD npm start
