# Importação dos módulos e classes necessárias
from flask import render_template, redirect, session, jsonify, request, send_file
from app.routes import artigos_bp
from app.models import User
from app import db
import uuid
import markdown
import os
from dotenv import load_dotenv
from passlib.hash import bcrypt_sha256
from datetime import datetime
