# -*- coding: utf-8 -*-

from base import *

class AipOcr(AipBase):
    """
        Aip OCR
    """

    __idcardUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/idcard'
    
    __bankcardUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/bankcard'
    
    __generalUrl = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general'
    
    def idcard(self, image, isFront, options=None):
        """
            idcard ocr
        """

        options = options or {}
        data = {}
        data['image'] = base64.b64encode(image)
        data['id_card_side'] = isFront and 'front' or 'back'
        data['detect_direction'] = options.get('detect_direction', 'false')
        data['accuracy'] = options.get('accuracy', 'auto')

        return self._request(self.__idcardUrl, data)

    def bankcard(self, image):
        """
            bankcard ocr
        """
        
        data = {}
        data['image'] = base64.b64encode(image)

        return self._request(self.__bankcardUrl, data)

    def general(self, image, options=None):
        """
            general ocr
        """

        options = options or {}
        data = {}
        data['image'] = base64.b64encode(image)
        data['recognize_granularity'] = options.get('recognize_granularity', 'big')
        data['mask'] = base64.b64encode(options.get('mask', ''))
        data['language_type'] = options.get('language_type', 'CHN_ENG')
        data['detect_direction'] = options.get('detect_direction', 'false')
        data['detect_language'] = options.get('detect_language', 'false')
        data['classify_dimension'] = options.get('classify_dimension', 'lottery')
        data['vertexes_location'] = options.get('vertexes_location', 'false')

        return self._request(self.__generalUrl, data)
