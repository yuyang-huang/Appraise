#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project: Appraise evaluation system
 Author: Christian Federmann <cfedermann@gmail.com>

usage: export_wmt16_results.py

Exports WMT16 results for all language pairs, in CSV WMT format.

"""
from datetime import datetime
import argparse
import os
import sys

PARSER = argparse.ArgumentParser(description="Exports pairwise results for " \
  "the given annotation project to CSV format.")
PARSER.add_argument("--project", action="store", dest="annotation_project",
  help="Annotation project name.", type=str)
  

if __name__ == "__main__":
    args = PARSER.parse_args()
    
    # Properly set DJANGO_SETTINGS_MODULE environment variable.
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    PROJECT_HOME = os.path.normpath(os.getcwd() + "/..")
    sys.path.append(PROJECT_HOME)
    
    # We have just added appraise to the system path list, hence this works.
    from django.shortcuts import get_object_or_404
    from appraise.wmt16.models import RankingResult, Project
    
    # Check if annotation project exists.
    if not Project.objects.filter(name=args.annotation_project).exists():
        print "Annotation project named '{0}' does not exist!".format(args.annotation_project)
        sys.exit(-1)
    project_instance = Project.objects.filter(name=args.annotation_project)[0]
    
    # Print out results in CSV WMT format.    
    queryset = RankingResult.objects.filter(item__hit__completed=True,
      item__hit__project__id=project_instance.id)

    header = u'srclang,trglang,srcIndex,documentId,segmentId,judgeId,system1Number,system1Id,system2Number,system2Id,system3Number,system3Id,system4Number,system4Id,system5Number,system5Id,system1rank,system2rank,system3rank,system4rank,system5rank'
    
    print header
    for result in queryset:
        if isinstance(result, RankingResult):
            try:
                current_csv = result.export_to_csv()
                if current_csv is None:
                    continue
                    
                print current_csv
            except:
                pass
