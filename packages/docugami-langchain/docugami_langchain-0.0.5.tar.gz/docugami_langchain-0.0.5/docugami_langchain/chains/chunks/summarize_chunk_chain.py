from typing import AsyncIterator, Literal, Optional, Tuple

from langchain_core.runnables import Runnable, RunnableBranch, RunnableLambda

from docugami_langchain.chains.base import BaseDocugamiChain, TracedChainResponse
from docugami_langchain.chains.params import ChainParameters, ChainSingleParameter
from docugami_langchain.config import MIN_LENGTH_TO_SUMMARIZE


class SummarizeChunkChain(BaseDocugamiChain[str]):
    min_length_to_summarize: int = MIN_LENGTH_TO_SUMMARIZE

    def runnable(self) -> Runnable:
        """
        Custom runnable for this chain.
        """
        noop = RunnableLambda(lambda x: x["contents"])

        # Summarize only if content length greater than min
        return RunnableBranch(
            (
                lambda x: len(x["contents"]) > self.min_length_to_summarize,
                super().runnable(),  
            ),
            noop,
        )

    def chain_params(self) -> ChainParameters:
        return ChainParameters(
            inputs=[
                ChainSingleParameter(
                    "contents",
                    "CONTENTS",
                    "Contents of the chunk that needs to be summarized",
                ),
                ChainSingleParameter(
                    "format",
                    "FORMAT",
                    "Format of the contents, and expected summarized output.",
                ),
            ],
            output=ChainSingleParameter(
                "summary",
                "SUMMARY",
                "Summary generated per the given rules.",
            ),
            task_description="creates a summary of some given text, while minimizing loss of key details",
            additional_instructions=[
                "- Your generated summary should be in the same format as the given document, using the same overall schema.",
                "- The generated summary will be embedded and used to retrieve the raw text or table elements from a vector database.",
                "- Only summarize, don't try to change any facts in the chunk even if they appear incorrect to you.",
                "- Include as many facts and data points from the original chunk as you can, in your summary.",
                "- Pay special attention to monetary amounts, dates, names of people and companies, etc and include in your summary.",
                "- Pay special attention to key facts like monetary amounts, dates, addresses, names of people and companies, etc and include in your summary.",
            ],
        )

    def run(  # type: ignore[override]
        self,
        contents: str,
        format: Literal["xml", "text"] = "text",
        config: Optional[dict] = None,
    ) -> str:
        if not contents or not format:
            raise Exception("Inputs required: contents, format")

        return super().run(
            contents=contents,
            format=format,
            config=config,
        )

    def run_stream(  # type: ignore[override]
        self,
        contents: str,
        format: str,
        config: Optional[dict] = None,
    ) -> AsyncIterator[TracedChainResponse[str]]:
        if not contents or not format:
            raise Exception("Inputs required: contents, format")

        return super().run_stream(
            contents=contents,
            format=format,
            config=config,
        )

    def run_batch(  # type: ignore[override]
        self,
        inputs: list[Tuple[str, str]],
        config: Optional[dict] = None,
    ) -> list[str]:
        return super().run_batch(
            inputs=[
                {
                    "contents": i[0],
                    "format": i[1],
                }
                for i in inputs
            ],
            config=config,
        )
