FROM node:20
WORKDIR /image-predict
COPY ./ /image-predict
RUN npm install @tensorflow/tfjs-node@^4.15.0
RUN npm rebuild @tensorflow/tfjs-node@^4.15.0 --build-from-source
RUN npm install @tensorflow-models/coco-ssd@^2.2.3
RUN npm install express@^4.18.2
RUN npm install formidable@^3.5.1
RUN npm install socket.io@^4.7.2
RUN npm install socket.io-client@^4.7.2
RUN npm install xhr2@^0.2.1
EXPOSE 8002
CMD npm start
