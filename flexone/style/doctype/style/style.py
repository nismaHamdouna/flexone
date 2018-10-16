# -*- coding: utf-8 -*-
# Copyright (c) 2018, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import os, sys, shutil, subprocess, logging, itertools, requests, json, platform, select, pwd, grp, multiprocessing, hashlib
from frappe import utils




class Style(Document):
	def validate(self):
		filename, file_extension = os.path.splitext(self.splash_photo)
		if file_extension !=".jpg":
			frappe.throw('The splash photo must be a jpg image.')
	
		filename, file_extension = os.path.splitext(self.icon)
		if file_extension !=".png":
			frappe.throw('The icon must be a png image.')


		bench_fo = os.path.join(frappe.__file__, '..', '..', '..', '..')
		site_name =utils.get_site_path()


		splash=self.splash_photo
		assets_folder =os.path.join(frappe.__file__, '..', '..', '..', '..','sites','assets','flexone','images')
		file_p = os.path.join(site_name,'public'+self.splash_photo)
		file_logo=os.path.join(site_name,'public'+self.icon)
		logo=os.path.join(site_name,'public'+self.logo)
		import shutil

		
		if os.path.isfile(file_p):
	    		os.rename(file_p,os.path.join(os.path.join(site_name,'public'+'/files/logo.jpg')))
	    		shutil.copyfile(os.path.join(os.path.join(site_name,'public'+'/files/logo.jpg')),os.path.join(os.path.join(site_name,"../../apps/flexone/flexone/public/images/logo.jpg")))
			shutil.copyfile(os.path.join(os.path.join(site_name,'public'+'/files/logo.jpg')),os.path.join(os.path.join(site_name,"../assets/flexone/images/logo.jpg")))



		if os.path.isfile(file_logo):
			os.rename(file_logo,os.path.join(os.path.join(site_name,'public'+'/files/icon.png')))
	    		shutil.copyfile(os.path.join(os.path.join(site_name,'public'+'/files/icon.png')),os.path.join(os.path.join(site_name,"../../apps/flexone/flexone/public/images/icon.png")))
			shutil.copyfile(os.path.join(site_name,'public'+'/files/icon.png'),os.path.join(site_name,"../assets/flexone/images/icon.png"))

			


		
		if os.path.isfile(logo):
			frappe.msgprint("s")
			os.rename(logo,os.path.join(site_name,'public'+'/files/logo1.png'))
	    		shutil.copyfile(os.path.join(site_name,'public'+'/files/logo1.png'),os.path.join(site_name,"../../apps/flexone/flexone/public/images/logo1.png"))
			shutil.copyfile(os.path.join(site_name,'public'+'/files/logo1.png'),os.path.join(site_name,"../assets/flexone/images/logo1.png"))
	
	




		self.splash_photo="./files/logo.jpg"
		self.icon="./files/icon.png"
		self.logo="./files/logo1.png"

		if self.background_color:
			sty="""
.skin-origin .main-header .navbar {
	background-color: """+self.background_color+""" !important;
}"""
			f=open(os.path.join(site_name,"../../apps/flexone/flexone/public/css/flexone_custom.css"), "a+")
			f.write(sty)

			m=open(os.path.join(site_name,"../assets/flexone/css/flexone_custom.css"), "a+")
			m.write(sty)
			
			#self.run_frappe_cmd('build', bench_path=os.path.join(site_name,"../../"))

			#import sys

			
			s=open(os.path.join(site_name,"../assets/css/flexone.min.css"), "a+")
			s.write(sty)
			frappe.clear_cache()




	def run_frappe_cmd(self,*args, **kwargs):

		bench_path = kwargs.get('bench_path', '.')
		f = self.get_env_cmd('python', bench_path=bench_path)
		sites_dir = os.path.join(bench_path, 'sites')

		stderr = stdout = subprocess.PIPE


		p = subprocess.Popen((f, '-m', 'frappe.utils.bench_helper', 'frappe') + args,
			cwd=sites_dir, stdout=stdout, stderr=stderr)

		sys.exit


	def get_env_cmd(self,cmd, bench_path='.'):
		site_name =utils.get_site_path()
		return os.path.abspath(os.path.join(os.path.join(site_name,"../../"), 'env', 'bin', cmd))

				



