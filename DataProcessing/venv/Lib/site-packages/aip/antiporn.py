# -*- coding: utf-8 -*-

from base import *

class AipAntiPorn(AipBase):
    """
        Aip antiporn
    """

    __detectUrl = 'https://aip.baidubce.com/rest/2.0/antiporn/v1/detect'
    
    def detect(self, image):
        """
            Aip antiporn check
        """

        data = {}
        data['image'] = base64.b64encode(image)

        return self._request(self.__detectUrl, data)
