# -*- coding: utf-8 -*-

################################################################
# xmldirector.bookalope
# (C) 2016,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################

import os
from Products.Five.browser import BrowserView

from xmldirector.bookalope.browser.api import convert_bookalope


class Bookalope(BrowserView):


    def upload_source(self):

        source = self.request.get('source')
        if not source:
            raise ValueError('No file uploaded')

        basename, ext = os.path.splitext(os.path.basename(source.filename))
        if not ext.lower() in ('.docx', '.icml'):
            raise ValueError('Uploaded files must be either ICML or DOCX')
        filename = unicode(basename, 'utf8', 'ignore').encode('ascii', 'ignore')
        filename = 'src/{}{}'.format(filename, ext.lower())
        handle = self.context.get_handle()
        if not handle.exists('src'):
            handle.makedir('src')

        with handle.open(filename, 'wb') as fp:
            source.seek(0)
            fp.write(source.read())

        self.context.plone_utils.addPortalMessage(u'Upload completed')
        self.request.response.redirect(self.context.absolute_url() + '/@@xmldirector-bookalope')

    def upload_cover(self):

        source = self.request.get('source')
        if not source:
            raise ValueError('No file uploaded')

        basename, ext = os.path.splitext(os.path.basename(source.filename))
        if not ext.lower() in ('.jpg', '.png', '.gif'):
            raise ValueError('Uploaded files must be either GIF, JPG or PNG')
        filename = unicode(basename, 'utf8', 'ignore').encode('ascii', 'ignore')
        filename = 'src/{}{}'.format(filename, ext.lower())
        handle = self.context.get_handle()
        if not handle.exists('src'):
            handle.makedir('src')

        with handle.open(filename, 'wb') as fp:
            source.seek(0)
            fp.write(source.read())

        self.context.plone_utils.addPortalMessage(u'Upload completed')
        self.request.response.redirect(self.context.absolute_url() + '/@@xmldirector-bookalope')

    def get_cover_files(self):
        handle = self.context.get_handle()
        if not handle.exists('src'):
            return ()
        return [ 'src/{}'.format(name) for name in handle.listdir('src') if name.endswith(('.png', '.jpg', '.gif'))]

    def get_source_files(self):
        handle = self.context.get_handle()
        if not handle.exists('src'):
            return ()
        return [ 'src/{}'.format(name) for name in handle.listdir('src') if name.endswith(('.icml', '.docx'))]

    def convert(self):

        convert_bookalope(
                context=self.context,
                source=self.request['source'],
                cover=self.request.get('cover'),
                title=self.request.get('title', ''),
                author=self.request.get('author', ''),
                formats=self.request.get('formats', ())
                )

        self.context.plone_utils.addPortalMessage(u'Conversion completed')
        self.request.response.redirect(self.context.absolute_url() + '/@@xmldirector-bookalope')

