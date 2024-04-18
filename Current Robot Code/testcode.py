import csv

# Open a CSV file in write mode
with open('team39_hazards.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    
    csvwriter.writerow(["Team: 39"])
    csvwriter.writerow(["Map: Demo"])
    csvwriter.writerow(['Origin: (2', '0)'])
    csvwriter.writerow(["Notes: This is the demo hazard info"])
    csvwriter.writerow([""])
    csvwriter.writerow(["Harard Type, Parameter of Interest, Parameter Value, Hazard"])
    
    # Iterate over each row in the 2D list and write it to the CSV file
    for row in careBotPaths:
        csvwriter.writerow(row)



# print("careBot took", careBotMoves, "turns")  # Print the number of turns for the first scenario



