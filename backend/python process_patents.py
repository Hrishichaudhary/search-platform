{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "289c3613-a2ce-4107-bf65-6f702849f6ef",
   "metadata": {},
   "outputs": [
    {
     "ename": "PermissionError",
     "evalue": "[Errno 13] Permission denied: 'C:\\\\Users\\\\Hrish\\\\Projects\\\\search-platform\\\\backend\\\\data\\\\raw\\\\patents.csv'",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mPermissionError\u001b[0m                           Traceback (most recent call last)",
      "Cell \u001b[1;32mIn[3], line 68\u001b[0m\n\u001b[0;32m     65\u001b[0m df \u001b[38;5;241m=\u001b[39m df\u001b[38;5;241m.\u001b[39mhead(\u001b[38;5;241m10000\u001b[39m)\n\u001b[0;32m     67\u001b[0m \u001b[38;5;66;03m# Save to CSV\u001b[39;00m\n\u001b[1;32m---> 68\u001b[0m df\u001b[38;5;241m.\u001b[39mto_csv(output_file, index\u001b[38;5;241m=\u001b[39m\u001b[38;5;28;01mFalse\u001b[39;00m)\n\u001b[0;32m     69\u001b[0m \u001b[38;5;28mprint\u001b[39m(\u001b[38;5;124mf\u001b[39m\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mSaved \u001b[39m\u001b[38;5;132;01m{\u001b[39;00m\u001b[38;5;28mlen\u001b[39m(df)\u001b[38;5;132;01m}\u001b[39;00m\u001b[38;5;124m patent abstracts to \u001b[39m\u001b[38;5;132;01m{\u001b[39;00moutput_file\u001b[38;5;132;01m}\u001b[39;00m\u001b[38;5;124m\"\u001b[39m)\n",
      "File \u001b[1;32m~\\anaconda3\\Lib\\site-packages\\pandas\\util\\_decorators.py:333\u001b[0m, in \u001b[0;36mdeprecate_nonkeyword_arguments.<locals>.decorate.<locals>.wrapper\u001b[1;34m(*args, **kwargs)\u001b[0m\n\u001b[0;32m    327\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;28mlen\u001b[39m(args) \u001b[38;5;241m>\u001b[39m num_allow_args:\n\u001b[0;32m    328\u001b[0m     warnings\u001b[38;5;241m.\u001b[39mwarn(\n\u001b[0;32m    329\u001b[0m         msg\u001b[38;5;241m.\u001b[39mformat(arguments\u001b[38;5;241m=\u001b[39m_format_argument_list(allow_args)),\n\u001b[0;32m    330\u001b[0m         \u001b[38;5;167;01mFutureWarning\u001b[39;00m,\n\u001b[0;32m    331\u001b[0m         stacklevel\u001b[38;5;241m=\u001b[39mfind_stack_level(),\n\u001b[0;32m    332\u001b[0m     )\n\u001b[1;32m--> 333\u001b[0m \u001b[38;5;28;01mreturn\u001b[39;00m func(\u001b[38;5;241m*\u001b[39margs, \u001b[38;5;241m*\u001b[39m\u001b[38;5;241m*\u001b[39mkwargs)\n",
      "File \u001b[1;32m~\\anaconda3\\Lib\\site-packages\\pandas\\core\\generic.py:3967\u001b[0m, in \u001b[0;36mNDFrame.to_csv\u001b[1;34m(self, path_or_buf, sep, na_rep, float_format, columns, header, index, index_label, mode, encoding, compression, quoting, quotechar, lineterminator, chunksize, date_format, doublequote, escapechar, decimal, errors, storage_options)\u001b[0m\n\u001b[0;32m   3956\u001b[0m df \u001b[38;5;241m=\u001b[39m \u001b[38;5;28mself\u001b[39m \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;28misinstance\u001b[39m(\u001b[38;5;28mself\u001b[39m, ABCDataFrame) \u001b[38;5;28;01melse\u001b[39;00m \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mto_frame()\n\u001b[0;32m   3958\u001b[0m formatter \u001b[38;5;241m=\u001b[39m DataFrameFormatter(\n\u001b[0;32m   3959\u001b[0m     frame\u001b[38;5;241m=\u001b[39mdf,\n\u001b[0;32m   3960\u001b[0m     header\u001b[38;5;241m=\u001b[39mheader,\n\u001b[1;32m   (...)\u001b[0m\n\u001b[0;32m   3964\u001b[0m     decimal\u001b[38;5;241m=\u001b[39mdecimal,\n\u001b[0;32m   3965\u001b[0m )\n\u001b[1;32m-> 3967\u001b[0m \u001b[38;5;28;01mreturn\u001b[39;00m DataFrameRenderer(formatter)\u001b[38;5;241m.\u001b[39mto_csv(\n\u001b[0;32m   3968\u001b[0m     path_or_buf,\n\u001b[0;32m   3969\u001b[0m     lineterminator\u001b[38;5;241m=\u001b[39mlineterminator,\n\u001b[0;32m   3970\u001b[0m     sep\u001b[38;5;241m=\u001b[39msep,\n\u001b[0;32m   3971\u001b[0m     encoding\u001b[38;5;241m=\u001b[39mencoding,\n\u001b[0;32m   3972\u001b[0m     errors\u001b[38;5;241m=\u001b[39merrors,\n\u001b[0;32m   3973\u001b[0m     compression\u001b[38;5;241m=\u001b[39mcompression,\n\u001b[0;32m   3974\u001b[0m     quoting\u001b[38;5;241m=\u001b[39mquoting,\n\u001b[0;32m   3975\u001b[0m     columns\u001b[38;5;241m=\u001b[39mcolumns,\n\u001b[0;32m   3976\u001b[0m     index_label\u001b[38;5;241m=\u001b[39mindex_label,\n\u001b[0;32m   3977\u001b[0m     mode\u001b[38;5;241m=\u001b[39mmode,\n\u001b[0;32m   3978\u001b[0m     chunksize\u001b[38;5;241m=\u001b[39mchunksize,\n\u001b[0;32m   3979\u001b[0m     quotechar\u001b[38;5;241m=\u001b[39mquotechar,\n\u001b[0;32m   3980\u001b[0m     date_format\u001b[38;5;241m=\u001b[39mdate_format,\n\u001b[0;32m   3981\u001b[0m     doublequote\u001b[38;5;241m=\u001b[39mdoublequote,\n\u001b[0;32m   3982\u001b[0m     escapechar\u001b[38;5;241m=\u001b[39mescapechar,\n\u001b[0;32m   3983\u001b[0m     storage_options\u001b[38;5;241m=\u001b[39mstorage_options,\n\u001b[0;32m   3984\u001b[0m )\n",
      "File \u001b[1;32m~\\anaconda3\\Lib\\site-packages\\pandas\\io\\formats\\format.py:1014\u001b[0m, in \u001b[0;36mDataFrameRenderer.to_csv\u001b[1;34m(self, path_or_buf, encoding, sep, columns, index_label, mode, compression, quoting, quotechar, lineterminator, chunksize, date_format, doublequote, escapechar, errors, storage_options)\u001b[0m\n\u001b[0;32m    993\u001b[0m     created_buffer \u001b[38;5;241m=\u001b[39m \u001b[38;5;28;01mFalse\u001b[39;00m\n\u001b[0;32m    995\u001b[0m csv_formatter \u001b[38;5;241m=\u001b[39m CSVFormatter(\n\u001b[0;32m    996\u001b[0m     path_or_buf\u001b[38;5;241m=\u001b[39mpath_or_buf,\n\u001b[0;32m    997\u001b[0m     lineterminator\u001b[38;5;241m=\u001b[39mlineterminator,\n\u001b[1;32m   (...)\u001b[0m\n\u001b[0;32m   1012\u001b[0m     formatter\u001b[38;5;241m=\u001b[39m\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mfmt,\n\u001b[0;32m   1013\u001b[0m )\n\u001b[1;32m-> 1014\u001b[0m csv_formatter\u001b[38;5;241m.\u001b[39msave()\n\u001b[0;32m   1016\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m created_buffer:\n\u001b[0;32m   1017\u001b[0m     \u001b[38;5;28;01massert\u001b[39;00m \u001b[38;5;28misinstance\u001b[39m(path_or_buf, StringIO)\n",
      "File \u001b[1;32m~\\anaconda3\\Lib\\site-packages\\pandas\\io\\formats\\csvs.py:251\u001b[0m, in \u001b[0;36mCSVFormatter.save\u001b[1;34m(self)\u001b[0m\n\u001b[0;32m    247\u001b[0m \u001b[38;5;250m\u001b[39m\u001b[38;5;124;03m\"\"\"\u001b[39;00m\n\u001b[0;32m    248\u001b[0m \u001b[38;5;124;03mCreate the writer & save.\u001b[39;00m\n\u001b[0;32m    249\u001b[0m \u001b[38;5;124;03m\"\"\"\u001b[39;00m\n\u001b[0;32m    250\u001b[0m \u001b[38;5;66;03m# apply compression and byte/text conversion\u001b[39;00m\n\u001b[1;32m--> 251\u001b[0m \u001b[38;5;28;01mwith\u001b[39;00m get_handle(\n\u001b[0;32m    252\u001b[0m     \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mfilepath_or_buffer,\n\u001b[0;32m    253\u001b[0m     \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mmode,\n\u001b[0;32m    254\u001b[0m     encoding\u001b[38;5;241m=\u001b[39m\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mencoding,\n\u001b[0;32m    255\u001b[0m     errors\u001b[38;5;241m=\u001b[39m\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39merrors,\n\u001b[0;32m    256\u001b[0m     compression\u001b[38;5;241m=\u001b[39m\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mcompression,\n\u001b[0;32m    257\u001b[0m     storage_options\u001b[38;5;241m=\u001b[39m\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mstorage_options,\n\u001b[0;32m    258\u001b[0m ) \u001b[38;5;28;01mas\u001b[39;00m handles:\n\u001b[0;32m    259\u001b[0m     \u001b[38;5;66;03m# Note: self.encoding is irrelevant here\u001b[39;00m\n\u001b[0;32m    260\u001b[0m     \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mwriter \u001b[38;5;241m=\u001b[39m csvlib\u001b[38;5;241m.\u001b[39mwriter(\n\u001b[0;32m    261\u001b[0m         handles\u001b[38;5;241m.\u001b[39mhandle,\n\u001b[0;32m    262\u001b[0m         lineterminator\u001b[38;5;241m=\u001b[39m\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mlineterminator,\n\u001b[1;32m   (...)\u001b[0m\n\u001b[0;32m    267\u001b[0m         quotechar\u001b[38;5;241m=\u001b[39m\u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39mquotechar,\n\u001b[0;32m    268\u001b[0m     )\n\u001b[0;32m    270\u001b[0m     \u001b[38;5;28mself\u001b[39m\u001b[38;5;241m.\u001b[39m_save()\n",
      "File \u001b[1;32m~\\anaconda3\\Lib\\site-packages\\pandas\\io\\common.py:873\u001b[0m, in \u001b[0;36mget_handle\u001b[1;34m(path_or_buf, mode, encoding, compression, memory_map, is_text, errors, storage_options)\u001b[0m\n\u001b[0;32m    868\u001b[0m \u001b[38;5;28;01melif\u001b[39;00m \u001b[38;5;28misinstance\u001b[39m(handle, \u001b[38;5;28mstr\u001b[39m):\n\u001b[0;32m    869\u001b[0m     \u001b[38;5;66;03m# Check whether the filename is to be opened in binary mode.\u001b[39;00m\n\u001b[0;32m    870\u001b[0m     \u001b[38;5;66;03m# Binary mode does not support 'encoding' and 'newline'.\u001b[39;00m\n\u001b[0;32m    871\u001b[0m     \u001b[38;5;28;01mif\u001b[39;00m ioargs\u001b[38;5;241m.\u001b[39mencoding \u001b[38;5;129;01mand\u001b[39;00m \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mb\u001b[39m\u001b[38;5;124m\"\u001b[39m \u001b[38;5;129;01mnot\u001b[39;00m \u001b[38;5;129;01min\u001b[39;00m ioargs\u001b[38;5;241m.\u001b[39mmode:\n\u001b[0;32m    872\u001b[0m         \u001b[38;5;66;03m# Encoding\u001b[39;00m\n\u001b[1;32m--> 873\u001b[0m         handle \u001b[38;5;241m=\u001b[39m \u001b[38;5;28mopen\u001b[39m(\n\u001b[0;32m    874\u001b[0m             handle,\n\u001b[0;32m    875\u001b[0m             ioargs\u001b[38;5;241m.\u001b[39mmode,\n\u001b[0;32m    876\u001b[0m             encoding\u001b[38;5;241m=\u001b[39mioargs\u001b[38;5;241m.\u001b[39mencoding,\n\u001b[0;32m    877\u001b[0m             errors\u001b[38;5;241m=\u001b[39merrors,\n\u001b[0;32m    878\u001b[0m             newline\u001b[38;5;241m=\u001b[39m\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124m\"\u001b[39m,\n\u001b[0;32m    879\u001b[0m         )\n\u001b[0;32m    880\u001b[0m     \u001b[38;5;28;01melse\u001b[39;00m:\n\u001b[0;32m    881\u001b[0m         \u001b[38;5;66;03m# Binary mode\u001b[39;00m\n\u001b[0;32m    882\u001b[0m         handle \u001b[38;5;241m=\u001b[39m \u001b[38;5;28mopen\u001b[39m(handle, ioargs\u001b[38;5;241m.\u001b[39mmode)\n",
      "\u001b[1;31mPermissionError\u001b[0m: [Errno 13] Permission denied: 'C:\\\\Users\\\\Hrish\\\\Projects\\\\search-platform\\\\backend\\\\data\\\\raw\\\\patents.csv'"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "import os\n",
    "\n",
    "# Define paths\n",
    "raw_dir = r\"C:\\Users\\Hrish\\Projects\\search-platform\\backend\\data\\raw\"\n",
    "abstract_file = os.path.join(raw_dir, \"g_patent_abstract.tsv.zip\")\n",
    "patent_file = os.path.join(raw_dir, \"g_patent.tsv.zip\")\n",
    "cpc_file = os.path.join(raw_dir, \"g_cpc_current.tsv.zip\")\n",
    "output_file = os.path.join(raw_dir, \"patents.csv\")\n",
    "\n",
    "# Read abstract data\n",
    "df_abstract = pd.read_csv(abstract_file, sep='\\t', compression='zip', nrows=10000, low_memory=False)\n",
    "df_abstract['patent_id'] = df_abstract['patent_id'].astype(str)\n",
    "\n",
    "# Read patent data\n",
    "df_patent = pd.read_csv(patent_file, sep='\\t', compression='zip', low_memory=False,\n",
    "                        usecols=['patent_id', 'patent_title', 'patent_date', 'wipo_kind'])\n",
    "df_patent['patent_id'] = df_patent['patent_id'].astype(str)\n",
    "\n",
    "# Read CPC data\n",
    "try:\n",
    "    df_cpc = pd.read_csv(cpc_file, sep='\\t', compression='zip', low_memory=False,\n",
    "                         usecols=['patent_id', 'cpc_section']).drop_duplicates(subset=['patent_id'])\n",
    "    df_cpc['patent_id'] = df_cpc['patent_id'].astype(str)\n",
    "except Exception as e:\n",
    "    print(f\"CPC read failed: {e}\")\n",
    "    df_cpc = None\n",
    "\n",
    "# Merge datasets\n",
    "df = df_abstract.merge(df_patent, on='patent_id', how='left')\n",
    "if df_cpc is not None:\n",
    "    df = df.merge(df_cpc, on='patent_id', how='left')\n",
    "else:\n",
    "    df['cpc_section'] = None\n",
    "\n",
    "# Select and rename columns\n",
    "df = df[['patent_title', 'patent_abstract', 'patent_date', 'cpc_section', 'wipo_kind']].dropna(subset=['patent_abstract'])\n",
    "df = df.rename(columns={\n",
    "    'patent_title': 'title',\n",
    "    'patent_abstract': 'abstract',\n",
    "    'patent_date': 'publication_date'\n",
    "})\n",
    "\n",
    "# Set field_of_research (prefer cpc_section, fallback to wipo_kind)\n",
    "cpc_mapping = {\n",
    "    'A': 'Human Necessities',\n",
    "    'B': 'Performing Operations; Transporting',\n",
    "    'C': 'Chemistry; Metallurgy',\n",
    "    'D': 'Textiles; Paper',\n",
    "    'E': 'Fixed Constructions',\n",
    "    'F': 'Mechanical Engineering; Lighting; Heating; Weapons; Blasting',\n",
    "    'G': 'Physics',\n",
    "    'H': 'Electricity',\n",
    "    'Y': 'General Tagging of New Technological Developments'\n",
    "}\n",
    "df['field_of_research'] = df['cpc_section'].map(cpc_mapping).fillna(df['wipo_kind']).fillna('Unknown')\n",
    "\n",
    "# Add placeholder for citation_count\n",
    "df['citation_count'] = 0\n",
    "\n",
    "# Select final columns\n",
    "df = df[['title', 'abstract', 'publication_date', 'citation_count', 'field_of_research']]\n",
    "\n",
    "# Extract up to 10,000 rows\n",
    "df = df.head(10000)\n",
    "\n",
    "# Save to CSV\n",
    "df.to_csv(output_file, index=False)\n",
    "print(f\"Saved {len(df)} patent abstracts to {output_file}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e6172792-105f-499a-bd61-f165f2cd9be0",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
