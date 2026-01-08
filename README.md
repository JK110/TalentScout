# TalentScout

A clean, modern platform to connect job seekers with recruiters and help organizations discover top talent faster.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)]

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

TalentScout is a lightweight recruitment platform designed to simplify hiring: post jobs, review applications, manage interviews, and match qualified candidates to roles using configurable workflows.

This repository contains the web application and API components required to run TalentScout locally and in production.

## Features

- Job posting and management
- Candidate profiles and searchable resumes
- Application tracking and status workflows
- Interview scheduling and notes
- Role-based access (admin, recruiter, candidate)
- Import/export CSV for candidates and jobs

## Built With

- Node.js / Express (API)
- React (Web UI)
- PostgreSQL (Database)
- Docker (Development / Deployment)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Node.js (>=16)
- npm or yarn
- Docker & Docker Compose (optional, recommended for local DB)

### Installation

1. Clone the repo

   ```bash
   git clone https://github.com/JK110/TalentScout.git
   cd TalentScout
   ```

2. Install dependencies for server and client

   ```bash
   cd server && npm install
   cd ../client && npm install
   ```

3. Create a .env file for the server (see .env.example)

4. Start the app (development)

   ```bash
   # from repository root
   docker-compose up   # optional: starts DB and services

   # or run services individually
   cd server && npm run dev
   cd ../client && npm start
   ```

### Configuration

- Copy `.env.example` to `.env` in the `server` directory and update values for database connection, JWT secret, and other environment-specific settings.
- For production, configure a proper Postgres instance and set appropriate env variables.

## Usage

- Open the web UI at http://localhost:3000 (or the port configured in the client .env)
- Use the API at http://localhost:4000/api (or configured server port)

## Project Structure

- /client — React web application
- /server — Express API and background workers
- /migrations — database migrations
- /docs — design, API specs, and architecture notes

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a pull request describing your changes

Please follow existing code style and include tests for new features.

## License

This repository is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

Project maintained by JK110. For questions or support, open an issue or reach out via GitHub.
