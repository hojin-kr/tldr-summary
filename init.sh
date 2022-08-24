#!/bin/bash
pip3 install scipy
pip3 install fastapi
pip3 install jinja2
pip3 install "uvicorn[standard]"ㅐ
uvicorn main:app --reload
