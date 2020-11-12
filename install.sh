#!/bin/bash

INSTALL_DIR=/opt/envs-logger

mkdir -p $INSTALL_DIR
cp -rv ./*.py $INSTALL_DIR
cp -rv ./envs-logger.service /etc/systemd/system/
