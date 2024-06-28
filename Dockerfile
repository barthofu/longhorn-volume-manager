# ==================
# == dependencies ==
# ==================

FROM python:3.12-alpine AS dependencies-stage

    WORKDIR /app

    # Copy app dependencies requirements
    COPY requirements.txt ./

    # Install app dependencies
    RUN pip install --no-cache-dir -r requirements.txt

# ==================
# ==== runner ======
# ==================

FROM python:3.12-alpine AS runner-stage

    WORKDIR /app

    # Copy app dependencies from previous stage
    COPY --from=dependencies-stage /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/

    # Bundle app source
    COPY . .

    # Start the program
    CMD ["python", "src/main.py"]