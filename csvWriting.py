def csvWrite(filename, rows, mode='a'):
  #newline needs to be empty string or the file will have too many newlines on rows
  with open(filename, mode, newline="") as file_to_write:
    csvWrite = csv.DictWriter(file_to_write)
    
    #don't forget to write header
    csvWrite.writeheader()
    
    #write the rows
    csvWrite.writerows(rows)
