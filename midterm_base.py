import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
from datetime import timedelta
from datetime import timezone



registed1 = pd.read_excel("registed.xlsx",)
registed = registed1.set_index('id')
print(registed)

new_df = pd.read_excel("new_df.xlsx")


