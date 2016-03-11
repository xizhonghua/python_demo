parser = argparse.ArgumentParser(description='Process some integers.')
  parser.add_argument('dist_filename', help="distance file name")
  parser.add_argument('-k', help="# of clusters", type=int, default=3)
  parser.add_argument(
      '-e',
      help="epsilon for DBScan",
      type=float,
      default=0.05)
  parser.add_argument(
      '-p',
      '--plot',
      help="plot the figures",
      action="store_true")
  parser.add_argument(
      '-m',
      help="clustering method [spectral, dbscan, agg]",
      type=str,
      default="spectral")
  parser.add_argument(
      "-b",
      help="score is stored in binary mode",
      action="store_true")
  parser.add_argument(
      "-o",
      help="output label filename",
      type=str,
      default="../labels.txt")

  args = parser.parse_args()
