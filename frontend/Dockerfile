FROM node:lts-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .

# Expose port
EXPOSE 4321

# Command to run on container start
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
