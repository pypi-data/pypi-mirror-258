from typing import AsyncIterator, Optional, Tuple

from docugami_langchain.chains.base import BaseDocugamiChain, TracedChainResponse
from docugami_langchain.chains.params import ChainParameters, ChainSingleParameter


class SQLResultExplainerChain(BaseDocugamiChain[str]):
    def chain_params(self) -> ChainParameters:
        return ChainParameters(
            inputs=[
                ChainSingleParameter(
                    "sql_query",
                    "SQL QUERY",
                    "SQL Query that was run by the system, to answer the question asked.",
                ),
                ChainSingleParameter(
                    "sql_result",
                    "SQL RESULT",
                    "Result of the SQL Query.",
                ),
                ChainSingleParameter(
                    "question",
                    "QUESTION",
                    "Question asked by the user.",
                ),
            ],
            output=ChainSingleParameter(
                "answer",
                "ANSWER",
                "Human readable answer based on the question, SQL Query and the SQL Result, considering the rules and examples provided. Please give a short one line answer, only "
                + "describing the result and not the query. Remember not to mention SQL or tables as instructed, just describe the result.",
            ),
            task_description="acts as a SQLite expert and given an input SQL Query, a SQL Result and a question, creates a human readable answer based on the SQL Result",
            additional_instructions=[
                "- Shorter answers are better, but make sure you always use all the data in the SQL Result.",
                "- In your answer, never mention SQL or the fact that you are producing a human readable result based on SQL results.",
            ],
            key_finding_output_parse=False,  # set to False for streaming
        )

    def run(  # type: ignore[override]
        self,
        question: str,
        sql_query: str,
        sql_result: str,
        config: Optional[dict] = None,
    ) -> str:
        if not question or not sql_query:
            raise Exception("Inputs required: question, sql_query")

        return super().run(
            question=question,
            sql_query=sql_query,
            sql_result=sql_result,
            config=config,
        )

    def run_stream(  # type: ignore[override]
        self,
        question: str,
        sql_query: str,
        sql_result: str,
        config: Optional[dict] = None,
    ) -> AsyncIterator[TracedChainResponse[str]]:
        if not question or not sql_query:
            raise Exception("Inputs required: question, sql_query")

        return super().run_stream(
            question=question,
            sql_query=sql_query,
            sql_result=sql_result,
            config=config,
        )

    def run_batch(  # type: ignore[override]
        self,
        inputs: list[Tuple[str, str, str]],
        config: Optional[dict] = None,
    ) -> list[str]:
        return super().run_batch(
            inputs=[
                {
                    "question": i[0],
                    "sql_query": i[1],
                    "sql_result": i[2],
                }
                for i in inputs
            ],
            config=config,
        )
