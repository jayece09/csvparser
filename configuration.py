class Configuration:
    def __init__(self, headers="headers.ini", normalizations="normalizations.ini", translations="translations.ini"):
        """
        Assuming suitable defaults for configuration files
        """
        
        # Sets the headers
        """
        Reads and sets the headers as a tuple
        """
        with open(headers, "rb") as handle:
            data = handle.readlines()
            tmp = []
            for header in data:
                header = header.strip()
                if header:
                    tmp.append(header)
            
            self.headers = tuple(tmp)
        
        # Sets the normalization paramenters
        """
        Reads and sets the normalization parameters as a list of dictionaries
        Format:
            [
                {
                    "header": ...,
                    "function": ...,
                },
                ...
            ]
        """
        with open(normalizations, "rb") as handle:
            data = handle.readlines()
            # The final list
            conf = []
            for param in data:
                param = param.strip()
                tmp = param.split('=')
                # The header to be operated on
                header = tmp[0]
                # The operation to be performed
                operation = tmp[1]
                
                # Currently only a single operation is supported, will change in the future
                if operation[0] == '*':
                    function = lambda x: x * float(operation[1:])
                if operation[0] == '/':
                    function = lambda x: x / float(operation[1:])
                
                conf.append({
                    "header": header,
                    "function": function,
                })
            self.normalizations = conf
        
        # Sets the translation parameters
        """
        Returns a translation table
        Format:
            {
                "Delhi": "New Delhi",
                "Madras": "Chennai",
                ...
            }
        """
        with open(translations, "rb") as handle:
            data = handle.readlines()
            # The translation table
            table = {}
            for trans in data:
                trans = trans.strip()
                table[trans.split('=')[0]] = trans.split('=')[1]
            self.translations = table

    def format(self, values=()):
        """
        Formats the input data according to our schema
        
        Takes a tuple of CSV values and returns
        the values in a dictionary
        """
        return dict(zip(self.headers, values))

    def normalize(self, data={}):
        """
        Takes data in the format provided by format function,
        and applies the normalization equations
        """
        for normalization in self.normalizations:
            data[normalization['header']] = str(normalization['function'](float(data[normalization['header']])))

    def translate(self, data={}):
        """
        Takes data in the format provided by format function,
        and applies the translations
        """
        for key in data:
            if data[key] in self.translations:
                data[key] = self.translations[data[key]]

