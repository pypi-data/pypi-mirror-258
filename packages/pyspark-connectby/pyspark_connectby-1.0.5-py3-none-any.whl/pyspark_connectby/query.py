from typing import Union, List

from pyspark.sql import DataFrame

from pyspark_connectby.connectby_query import ConnectByQuery, Node


def connectBy(df: DataFrame, prior: str, to: str,
              start_with: Union[List[str], str] = None, level_col: str = 'level') -> DataFrame:
    query = ConnectByQuery(df=df, child_column=prior, parent_column=to, start_with=start_with, level_column=level_col)

    return query.get_result_df()


DataFrame.connectBy = connectBy
