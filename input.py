import simplejson
from csvio import UnicodeReader, UnicodeWriter
from configuration import Configuration

class PrepareInput:
    def __init__(self, input_csv="input.csv", output_csv="output.csv", output_schema="output_schema.ini"):
        self.input_csv = input_csv
        self.output_csv = output_csv
        self.output_schema = output_schema

    # Applies configurations and outputs CSV
    def output(self, format="json"):
        csv_reader = UnicodeReader(open(self.input_csv, "rb"))
        csv_writer = UnicodeWriter(open(self.output_csv, "wb"))
        schema_reader = open(self.output_schema, "rb")
        schema = []
        config = Configuration()
        json_output = []
        
        tmp = schema_reader.readlines()
        for header in tmp:
            header = header.strip()
            if header:
                schema.append(header)
        
        for line in csv_reader:
            # Cleaning is missing
            
            row = []
            data = config.format(tuple(line))
            config.normalize(data)
            config.translate(data)
            
            if format == 'json':
                json_output.append(data)
            
            elif format == 'csv':
                for header in schema:
                    row.append(data[header])
                csv_writer.writerow(row)
            
        if format == 'json':
            simplejson.dumps(data)

if __name__ == "__main__":
    obj = PrepareInput()
    obj.output()

