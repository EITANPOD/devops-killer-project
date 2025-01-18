# Recipe Website Project

Welcome to the Recipe Website Project! This repository contains the source code for a full-stack web application where users can add, edit, and delete recipes organized by categories. The project is designed to showcase DevOps skills and modern cloud infrastructure management.

---

## Table of Contents

1. [Features](#features)
2. [Architecture](#architecture)
3. [Project Prerequisites](#Project-Prerequisites)
4. [Tech Stack](#tech-stack)

---

## Features

- **User-friendly interface**: Easily navigate and manage recipes by category.
- **Recipe management**: Add, edit, or delete recipes effortlessly.
- **Category organization**: Group recipes by customizable categories.
- **Cloud-ready**: Fully deployable on cloud infrastructure with robust CI/CD pipelines.

---

## Architecture

The project is divided into three main repositories:

1. **Application Repository (this repository)**: Contains the source code for the frontend and backend applications, GitHub Actions CI, as well as API and database integration, and Kubernetes manifests using Helm.
   - **Frontend**: User interface for managing recipes, developed using JavaScript, HTML, CSS, and an NGINX configuration file.
   - **Backend**: RESTful API built using Python to handle application logic and database operations.
   - **Database**: PostgreSQL database hosted on AWS RDS for data persistence, provisioned using Terraform in the [Infrastructure Repository](https://github.com/EITANPOD/devops-killer-infra-repo).

2. **GitOps Repository**: Stores the main Helm chart values, and an `application.yml` file for managing the ArgoCD configuration per environment. [GitOps Repository](https://github.com/EITANPOD/devops-killer-gitOps)

3. **Infrastructure Repository**: Contains Terraform code to provision the cloud infrastructure, including the EKS cluster, RDS instance, and other resources. The Terraform code is organized by environment to ensure flexibility and separation of concerns. [Infrastructure Repository](https://github.com/EITANPOD/devops-killer-infra-repo)

---

## Project-Prerequisites
- Docker
- Kubernetes (with a configured cluster, e.g., AWS EKS)
- Terraform
- ArgoCD (for GitOps management)
- Node.js (for the frontend build)
- Python (for backend development and API setup)

---

## Tech Stack

- **Frontend**: React.js (using JavaScript, HTML, CSS, and NGINX configuration)
- **Backend**: Flask (Python)
- **Database**: PostgreSQL (AWS RDS, provisioned via Terraform in the [Infrastructure Repository](https://github.com/EITANPOD/devops-killer-infra-repo))
- **Containerization**: Docker
- **Orchestration**: Kubernetes (AWS EKS)
- **CI/CD**: GitOps (GitHub Actions & ArgoCD)
- **Infrastructure as Code**: Terraform
- **Cloud Provider**: AWS

---

## Tools Used

This project was built using the following tools:

- Terraform
- Kubernetes
- Docker
- Helm
- JavaScript
- Python
- GitHub Workflows (Actions)
- ArgoCD

---

Feel free to reach out with any questions or feedback!

