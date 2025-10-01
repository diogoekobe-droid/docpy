import re
import datetime as dt
import pandas as pd

def document_record(supplier, filename):
	today = dt.datetime.today().date()
	id = extract_int_prefix(filename)
	record = {'FORNECEDOR': supplier, 'ID': id, 'DOCUMENTO': filename}
	if filename.endswith('Indeterminado'):
		record['VALIDADE'] = record['DIAS'] = record['SITUAÇÃO'] = 'INDETERMINADO'
	else:
		date = extract_date_suffix(filename)
		#print(date, dir)
		if date is None:
			#record['VALIDADE'] = record['DIAS'] = record['SITUAÇÃO'] = None
			record['VALIDADE'] = record['DIAS'] = 'N/A'
			record['SITUAÇÃO'] = 'OK'
		else:
			date = pd.to_datetime(date, dayfirst=True).date()
			record['VALIDADE'] = date
			record['DIAS'] = delta = (date - today).days
			record['SITUAÇÃO'] = 'VENCIDO' if record['DIAS'] < 0 else 'OK'
	return record

def document_table(records):
	def highlight_red(row):
		condition = row["SITUAÇÃO"] == "VENCIDO"# or pd.isna(row["SITUAÇÃO"]) or row["SITUAÇÃO"] == ""
		return ['background-color: red' if condition else '' for _ in row]
	df = pd.DataFrame(records).style.apply(highlight_red, axis=1)
	return df.to_excel(f'LISTA DE DOCUMENTOS PRESENTES - {dt.datetime.today().date().strftime("%Y-%m-%d")}.xlsx', index=False)


def extract_int_prefix(s):
	"""Extracts leading integer from the start of a string or returns None if not found."""
	match = re.match(r'^\d+', s)  # Match digits at the beginning of the string
	return int(match.group()) if match else None

def is_valid_date(date_str, dayfirst=True):
	print(date_str)
	try:
		#parse(date_str, dayfirst=dayfirst)
		pd.to_datetime(date_str, dayfirst=dayfirst)
		return True
	except Exception:
		return False


def extract_date_suffix(filename, dayfirst=True):
	pattern = r'((?:\d{1}|\d{2})[\-./](?:\d{1}|\d{2})[\-./](?:\d{2}|\d{4}))$'	# Matches "dd-sep-mm-sep-yyyy" or "dd-sep-mm-sep-yy" at the end
	match = re.search(pattern, filename)
	return match.group(1) if match and is_valid_date(match.group(1), dayfirst=dayfirst) else None
