# 使用 Node.js LTS 作為基礎映像
FROM node:18-alpine AS build

# 設定工作目錄
WORKDIR /app

# 複製 package.json 和 package-lock.json
COPY package*.json ./

# 安裝前端依賴
RUN npm install

# 複製所有前端源碼
COPY . .

# 編譯 React 應用 (production)
RUN npm run build

# 第二階段: 使用 Nginx 作為前端靜態文件的服務器
FROM nginx:alpine

# 將編譯後的 build 文件複製到 Nginx 靜態目錄
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
