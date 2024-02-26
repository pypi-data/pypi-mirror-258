# coding: utf-8
"""
    Harmony Endpoint Management API

    <h2>Today more than ever, endpoint security plays a critical role in enabling your remote workforce.</h2> <h4>Harmony Endpoint provides comprehensive endpoint protection at the highest security level that is crucial to avoid  security breaches and data compromise.</h4> <p>The following documentation provides the operations supported by the Harmony Endpoint's External API.</p> <p>To use the Harmony Endpoint External API service:</p> <ol>  <li>   <p>In the <em>Infinity Portal</em>, create a suitable API Key. In the <em>Service</em> field, enter <em>Endpoint</em>.</br>    For more information, refer to the <a     href=\"https://sc1.checkpoint.com/documents/Infinity_Portal/WebAdminGuides/EN/Infinity-Portal-Admin-Guide/Content/Topics-Infinity-Portal/API-Keys.htm?tocpath=Global%20Settings%7C_____7#API_Keys\">Infinity     Portal Administration Guide</a>.     </br>Once a key has been created, it may be used indefinitely (unless an    expiration date was explicitly set for it).</p>   During the key's creation, note the presented <em>Authentication URL</em>. This URL is used to obtain <em>Bearer    tokens</em> for the next step  </li>  <li>   <p>Authenticate using the <em>Infinity Portal's</em> External Authentication Service.<br />The authentication    request should be made to the <em>Authentication URL</em> obtained during the previous step.</p>   <p>Example (<em>Your tenant's authentication URL may differ</em>):</p>   <p><img     src=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAa0AAACSCAIAAAB5bwKsAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAB8OSURBVHhe7Z1PaBzHnsd7lz0NjAVW9tALA2MIVsDhGVayzPDIBoccdDDPQbwoKPhmDLEvEu+uHJ7uD+liB4xvJsZ2EPHig2BDjAlhsCwfvNiQMQYL5tCHfTLYA3Pe3+9X1V3V3dU9PTOtv/39MKCeUk/9r1//qrrr2/8yPT3tAQBAhflX/RcAAKoK7CAAoOrADgIAqg7sIACg6sAOAgCqDuwgAKDqwA4CAKpOqc8Pfnvz8d/O1fmo9+wfF679KIGFWHmwfelU79nahWt3YsduZu8ttZpB+/z9Lf7WmPtlfkpSJfrPN25d79JB48bV+emahDnP5MDAnKPod9Zubd7lo3gSLr5/sP2Xj4YsJgDgMFKqP/jjtQszM2vbPf11CFa//u+3Xv3cpe+9yz98cYrM6K1MI0gEu32v9yHQ34Sd9vr59fVHQW16fmGF7OrC/LTXWVtfP7/R6fmte7N0yuy9+Smvs0Gn8YcNXPf6LTreeN4Xs0iB2ggSjiQS/P3hs1793DwlBgA42jjt4OWbj7c1P/E4X/lpe/vxzct0RB7f9vaD7znsAYX99ECfKKeNxd+/frjjnbrw+MpMvbd9e0Qna3WHLNeE/59zn/vezgsxat1Xr/tesznrNU5OqpPK4s61x2+95p9gCAE46qTtIBnB5XPes7UZ4a+rOthFven9SueQK9f84ua3OnBkVjfIwarXvbe/fpfjCzLsx325ybPfBCtN3+t3f/s//VXoBu/JNp5c7G4+Cbz61PzTpaWnC+wf5pKZhA27hKe++IEvEACAo0vKDn7750/IFD3Om5ZG9LYfspn8+9czM8Mtk13+IXI4HxsD+vFHsnb30X+MYFKbrSUycBf94JGZ2yZZvU+z4PYOHfmtp0s8fR6XO793evWZS3AJATjSHMz94jvfXVDupmVAL9+8cMrbecaLbldlDj4Uan3w/Pp9t//6/l1oHLe+WV9f6/R5+tzQQWNw57tf33pwCQE42qTs4I+//9HzTl1wW6KVeXU7uHwu/3DlXL33bOMaL7rJDZMxUGuCZ+cW6bgha4U7sdu+H5+okWkMBsx6i7H6cLtXn/ozDCEAR5e0P3jn2oWHb+vnltW0VW6AyModh1zy3r5VZzn5/gH9YnmGTGX93N/CWytF+PbmFfrVzq/sG/Kim3fqLw/GmWx2r99q79SmlpeWnso94m/IDDbmfqGv8rno959vZHiOQ8Mu4biGGwBwkEB/sARWftq+NJn3wCMA4DADOwgAqDoHc58EAAAOD7CDAICqAzsIAKg6sIMAgKoDOwgAqDqwgwCAqgM7WDqzC0+Xln6ZK2HXHjhAFueuUjuKYhs49oxlBxs3ri49vSrb14SVhdjXkNl7abvAxuLqjbJthSsDrtQjxGbJZwzZBdmpMsKA4dyq1Afr3xxSxFgMqDplUPjj6Bv55LbdAMb5bXFkCOxL8xWp6hTJSsgYoZpSkigbjl/1n/gQk/DcmjcigYMZyw6KpJWRMDho1FZiJTsYsjh3tukFT7IUtLbui3qr/lYOEudAzS6dWyUPka16fQy4u3lLi90eKSTb67wj81Aw+9VUrddpl7QZ1Mk+JDECLIxyvp0eooOVkn+89itLmhba3TvefhK6vFz0jHg9f50Idjy/WdMa9x9TiK/+KXDgu6+WWk39nel1Nr7c9O8ttbwgaPp8toSwHeEI9c+DR5GWjJLXT4nmS+qRsL6CLhqtyTA2wkRoJPhVoBV/WtNfUtxt86iwUrFOE8Gbb7ZMSFQEusYuN97rOrFLQa5oayJ8iwB/56wGgef7LGUh6fJvp8IE8l4SEMsJp9L2Lra8eFrWVwsujhfs+D63SFQn1gsMpFw6tzuB1/Q5GQ4M7NchMHImlyJs3OgdCYTk0Eu0TopkurE6iarUOs1KgnOom1YCo6b3pHI48LczrrZIF1baQpUiDHFUlGe3DmN3oSSOjpfIsEfZaHj9Wr3WV/Vsyqt60dR7Hb/5YRRbVNhudKYXpaiQM3k8xkdo1ByxJPRXKZ06TRJVWVL/opp52XQkQRGawupOG2tH07eTbZEeUPpYFTkWIief7poqcsJvCvnkjwIvzxhvfZAV/RKDs+Z7L0QNvzb11ayR/KMaZMeHqyky8NT87A1FJWn6NFb5X/WpOZ4yzy6IIEKuoJZh9tOUM+jNNm1nUJqHalwitHpAgoSmf5bPHztNh4nQv/kaUvMnu1R8qgf/c46NusWSdOXa9Dw5/GZ9oO57TyhCqhz/LAUql4Q/5u0CDhbn5qZrUi5OmmrMVVf9D2/0UQq69rBbysoUV1T2RJyC0l3r9JutKHu1pveCAsl9Zi2f7uaXWsFMV6n0UWlc+fA7EuaGmQiLPYpenBD1eFUnlFB9qiVTNs4eXZPonLWOp17DEI0T+W1kfBmpHDE0KlC3Bfmn/kWeVTkLm+GDqIqiSpa+bfxcGticbmYXdXQ8KmyY4ehlEpS53RcUIdczl/dEZGManzUsT00mHPKJmsyBa+gJ8REaEk9idkFsIsWw8dybWqaK2rovTUADk91GZZKcSZCBY0dBZc8aPom+zSTHhXpPBn+kLfJn6IWUktklLPTyjNLvk/Q7P8cNY3F0MwQfel5tkvqAHLClSKxoyAhM2F+e/yaTbtw4S1ewyM9nQ1nA7ZfTuq+404h+l9UdbazTBpOYmCeuBGbc6uxxR1eBYjHpY3teNOZVoL1ikjBzXHUTfoOumbx2s3hyIm/5QtcbTzS4sHzx6L9+xcnffdXVbcH0n7f5PO792VcRGgYqbzFPoQCLZxp11wpGssk4e1p2N3LHRIfc0fHqU/PiudiWUSURqpRnFtbFiH3b0fFUYV9KbPplEv9Oh/1dsb16ukfZ4z8UQYuuc1bNcLNKJcfmVUVxliKeBNen51/kJIyDRnZfTDa/v8zyyxKwPfWU1FNy2pfo20SqucO+HXe0x2H1fwup5R/m+8WRxyHVmnsjQpY2ElaJm1Z38aMJdfcWGfe4y2m7A9pp4gEciozVgxfcybrvdukf/pnT74PdxpmPo6G117Afwc4C5a3kVdcY0SyBPnkThV4QUL3x22mOMHw5pxl5VEyeiCj3X3yxMkgmwaiOpz7a52j4E/J3INpB5s9Al80gPrJyLXnUl0Sx96kdPju40iLfR18qCZ59iBWYPBn6/1RfNOatW0WumyGqacUoaLZe8vtJ1NwqB3GLGmf4Utw4c7oW13CVmxtC6D3pDO8Z4sflJ8H/jXqe7rKUvdrps43dnfau1/i8Udt9pyuC5mh0vXVcVPiyIYUVN/z0Ga5t220pjDg1pqIyUZ5jNG8Sd0zNj3JRs4RWrADsUsVmeSEf2rdpRKWXFCR7fOEct7BOlBcfTescHe/uO3JH/U8lV66X6ljI5Vx54gZx/6XbJ2CHQB8WJ5XEmw/sfCTqk1cYeCEoNttNIY52NPMdHumoI5Uii0LvU9sPO7j1M68syAuSohnuVvt5X62OmZGgzjEiqdEEkNycfud25oUlvrShYBOW7D2r92VVSMUpOVFDUWZwEs621aXhKu944rnYfGM3UFeq7vVNXrPjn9OVVIIoxzwAZA4rZRnzwaDu9ReBvEpl6fMPnZwr/2pb50R9pD65O9Zr3m7Q/a3LB3mowsqlWBX2S16i5bZYnvLyBWvvbr7Y0RMosa1Rs86feB1e0sXyyvRKEsocQla6OjYncpqqFv6oHiWrV2qynKh2mc1x24URSm7ZcW6zq+IsrLrQyr0IiTNnocq0Uc5p6Y5nZzj/pTpsJWOXc2luqcnlE93wLnw0xPhmowoSXEMvRTqJqNKkXNxkfFuDPH1ef9dxhu2YTEIKq4c2fTLbMU00ypbO7nbCUgzRFpkUeJ/aYdEflDtK1g2yIeA18uTNUF6Ztm5kH2vkLtt7XVguePKmeR7Dnn+kkcFsbokeAcgKzDdem9vue8A+JHHwXP7h8fLMPx/OfJ3V8sfADlYeda3WX3jtbIg+DTsIAPSoAQDgMN8vBgCA/QB2EABQdWAHAQBVB3YQAFB1YAcBAFUHdvDAkIeus59uHRK153SUp0wzkefYMx97BuD4UKYdXPlpe/uxVvu6/ANrIOaMShm3pVmBgkiiudqN5WNkEcoyUntTCnlwf4in/4dDjH5unodRzQSgXA7MHzxkGq57h8giuEQHRHWmtAeYlWbR6E8I8yblhBKJ5LykJ9vLVc0EoFzKfI6a/MFLk8/WLly7U2AjS2Lrm2wOC/dEGMFF3vSjJQZMIG+kU5v4w70T5jQdwjsH4iqPb2KbLggOlMzxVhaWdckzSXKOPtZJSP4TCqZ8WlpNluCTLalXswMklq5VCZFWZZTndAgjcZoKMUmkY1M7qHYDS0s1snpSgUpoNl5YUwopggqLUimeBJ9ZnmomAOVSth2MCWC8zbODWZjNTzI4vcRmOxnzsTGsrI+ERL9VVk/GsMgR6+23Mm7DrbghReygIdqIpqS2JSccg2wKZFXtprFNRm46YQcFyYyRaE58jROzU85SJJOI8nk3qsZXZ/hqISUVXWKTFtdbo5tM2q7/eHEUQyVRDO5C3sOZvw7dawAYh9HnxbICqHhsZA57z9ZmmLXtpCjzIGikyTpa5O84hTkdipsuYU5B/TZU3NSBaQrNT8lSqOzF5EV1TowGF6GVb0TQKU/UM4HS+EroabONlrXF0CkuTKaabCoJQhSGHeEWSu0qpok7VBIFKaiaCUC5jG4H73x3QSweMf5EhhyKsSQYaa6qdR/HWSPLZJ/kRROQ3+fSYS0bpd44QHdvCE3csSimmglAuRym52YSEoxOYU6H4qZLmNMQKW7q72nE5xp85zpbXjRSMLVIqMkORlwqfu+H/h5SQIfVRa6abAyR8k6oN2YQ18QtnsQwFFLNBKBcDokddEowOoU504qbTmFOJq64yRRSzXTgkhdlEgqmgspwpCarJtRxqVdeWUtJk1r6r/q0LB3WZClcSbjUZJ3EX2WVSbhqwfWpNXELJzEkBVQzASiXY6q7Fd0w2bsFd3OXQAcQ0Q2TQWblsMC3XDJv48Zuzuwngx82AKBUDtO8GOw7/NRh0giS+QtdvxK9vGGQpWcYQbB/QIcVAFB14A8CAKoO7CAAoOrADgIAqg7sIACg6sAOAgCqDuwgAKDqwA5WDLX5pLwNwgV3JRanUb6wNgADKNMOjqtHLbvN1Ec2zA0Bj8YRFeR5x9iA5CKxmVGzdwCYPJdlpApU1AhIPvfM6sl2wFyjb3daUFkOzB9M6lHzNjWWz1OaMTGduwOH9QW0EI7K4eHKnhPJ88bzlHaPKkt5u0TGVNVOqzyMK6wdgzU4RCAjk9UNFri5hPcBVJtDokdtS35aiHGUo1AnVX4VU4FWeqiG8EzZYizSNTqEN//GxaKVbKoh0l52IhGGe5bje285V7zX+N1XLj3qVE4EiaGuZJwzMD8k9JnpUnT5tLj4dljpothqtF35t6q8MSFbcppi+t7yqzDZSGg2XVHuciVjczSZPjNepbHCOiWvo98WT4IrufE6Lh+bAuKvoGx/sH5uWaRZl2cGCUWt3l83JsA/QaeL7paBBkboIYquSfSWHzIBbZHkEwEujodOkMHJvmQ4VGSA0b82nnvmt03fo0Dy7OpTrRXly7TJW9DyhTlGMImSyWpKtCLGFYmPqiQo2vrUHM8iM3JSBOW78YcK67ei+V0yCaLmT3ap+OQA+hczk4jKayE2RUkrhn6u8sj4I9I+NGl1V5TD5SS7E8b2KKhNz4cT3niThTQ+axhnMCqsrfC4ODc3XQtnCaplh0qCZRPzjSDBLiHEX6vN6HawbD3qJDxI6Bovg2TrJY2NSFM6oUftgmWrlQiVkrcKKSa0x6uNenEt06Yo8asmDUKlmx1JDSb0qLNyopRNc5xBIcxJXI86kYRQUHw7iUPfm5BlNfpYDloh7KpgpUhvwldm2tlkrNs4QPLr7jsqj9ErI4ZLohg//v4HxF+rzeh2sFQ9ah7SSt2zPGh+pPyIweYmgbg/A3+4tUNT0U9nY06NmxFzQlPC/dCjTiIOl3KuZUl0j2jcOOuH17lsorf9sd7int2eUuKvcAmry4HdJ4mjXnDBc9UIcW3E4SLPwbwKoxhvPrCCfEy2uny2fuZpI3l5Dqcm0qPOzAmZG8vNySRbj9oheT1YfDuJQ99bSGiDF0S5b59KbOJpdn/L8vbYGew/bxe6KvDSB8/K2fkdIolhkPcBfPJfuG9cUQ6JHeQ1KVnbUtNAufKv3o9CWk2jKe2ETZJWrpbHRO5u3iInIpStXsp7pCbSmh7+yRt5cwA5szGnJqFHPUROkmTpUSeTEKSiLPHtlbTktbK8codB8iMray59b4c2OJGqKEcSVmy8tmvdEknAJix4MWjljteIJWOS7aDN93YKJzEc7BLWZy5hblxNoD84DnyTwX6bJd9X3WM9akcS9l3XowFZ5OzbuOHN95IMXHFWHmxf+mh77cJ3d3QAqAyHxR88amjfKvlKX1AI121c8S7L9vKGYvXrmRkYwWoCfxAAUHXgDwIAqg7sIACg6sAOAgCqDuwgAKDqwA4CAKrOIbOD6uGJYZ9nBgCAMdgjO3j55uPt7Z/yHs536LB6swuyR2IY3RcAABiXA/MHkzqsIe8D2EAAwL5Ssh0MxbiWzw2SHwQAgENCqXbw+wfLM96zf8zMzKw9G6gTFdNhFRZPTnj9D2/0NwAA2B9Gt4NpHdaVP53yen/8PpIWIQuOLp94McabLgAAYDRGt4Ol6rCK9Onah7OlvgESAACKUOa8+O0/e179o1N09P2lUdYHWWKzduJj/Q0AAPaHMu3gne9uP+udukQT5b94b23dUAAAOMQcKt0tljX1jpKeKADgOFDq/eJx2br/KGB9eewnAQDsI9BhBQBUnUPlDwIAwAEAOwgAqDqwgwCAqgM7CACoOrCDAICqc2B2UPQHlxbyJAoBAGA/GP25mdl7S63JzsZtb2650V3L1Efg05pytNNe/8boy5AdnJ+uBSM8Nb04d3V56r35YWPul/kps42v34llRv67K0mHP9z5dKnlxTIzmJWFpYsTnbVN78p847W8u11iq6n/9joblnZsVpFtVPHlUGfY/IqwI+SkfTkK2kqhxyQdhjD8FLpvFT8doWcSFUwq8tvoq0lRYaeio+2rF9jblUDnRY2SyqHJjEnUapqI8WrVynmiGyRQdcXogghREirQaqPYaXaXC8NNSE4lZFGoaOkk0n0SjMq/6b/DE+z2vUl9nMPWN+tbVreL6F6/ta4Px6S7+eX6pvQ5yzi6uPvu/bI+HJo3H/rehD5W3N28dXeTDyTpuRuvdEdcnDvbtAaDk5WF+Wmvs7auzd+VuVcqKscwaMx97sfCZahT/Lfi8c/eI0PW7ye2dScijOpc8uy9fsU5tk2PYvX+uo5cGm5nx0SxstBq9vs9+/SUxUnnkOtE2QKO0NRVmnFqVepKnRPVqisZMihUKKkZzurc3CLlX6yM19k4b34SdVExiOo0+b7SmqrbpVa11F7/0qrqjGZyUKhoriTSfRKMynjz4t13qX5GDbbE7xh5unT1RtauEHOOPS+mvqsCl+7N8ncaCU+vLtzj6XN4JnXWpSUZtLztJDrThZp3Lz21XUXCoW8o6RbRuXGoZ0cYGe2PT9RiqZjCxlOxFCUc1Rjhn6h7/d1Af6PoPmWzmBwzYp46T7KjidP4rFHzghdiYma/4utH27kffKXJDubP0dhTL054kZ+MI4dk3bRDFHzoebVJ+5rY1PXjasrsWiWkM8R+y1dElS5fpOsnwmQSfdKq0tWdwKtRbXiLZxpk2m477abCtH7DJ+tjdQaupaAdv4C5mimjJ6SKZgZCNIhcSQh5fRIUp9z9JNTS4ZU2his8vGCqvsKX3NNdmQfxyRM03fjtDPspMjny6fJOc3A1SxJPIen6JQI5cpoyhNf5xOQrDvsOZETyplFuzLxJF02KKf8SknFyQmEpJFEVnJo5hhMfO4SQKZgnxQmCps8J6Zkjl5FnRlxjZo0iHWGIoznsvIWELlIYGLbRqzMqOTKjti9pZSaVwxA534vNJaWWPNN8xWo1mbc49n/ThbVCovwELeowwY7nNznpsLpUDvk3OsQuL8NtF3CG3wc7vs+1bWUvqxJMbb9r5XaYqBu/+iydhDoDlEOp90mS7kNxGmdO17z61DxfA2Mz6OCJs6MPgK/Gve6rYn2FpQ9H0n/ledN5+m07aLbEJdm6T18fkaNBPdXEGXqmtlFrnDRLCv5ZueZLNviz8bzvX2R/QULaHN3zDQoX28G+jNf0dujMtU6/TjPHRuPG3FRdO3cK5R2lI9QUbCZ2kaz6X5ybm64lm4MdPZVKO6Dm40pw5FCfTGblCl/YNq2sejsvuJZYcs2b8PnMQrWayFscqZDQuXMUlrexexQ5NcoVnTdx8WoTu5uUNLnG/sUFqUN2MDkzsu2dZyRSXqpPsYD0L76A+ZNkGH3vJX3d6PRqU1fmGhmVkOoJ7g7D1lZOC9c6nUmAMjlMz83QJZr7Fn8y148OI1s7NKmcPOnumrwUyLeD1ABTKMslA4kDa9MtZbkU8garLHhe6akFu7uvujzH/IQvIZ7fomHDrkptankpYeHiEcqCY4GLBM2Xae68E3qRMpVWyxHsItWm5+MzWclYdBDLoRrM+R5cmtxazUbcSW+Ax8TvhJCedpvzQrNvqaJ+9zf+uvWSDNPESXudhKfP2kyn4Tm4rqjuq9dqPu6qBFdPcDG7QO2oxgKbSMaVBCiTUu2grLZMfWUPj4J03+3S9fNsgUW6QpjlIV7SVmGZ0CSl2PpgBrLOnbvGJ6s/6jSDNdJ6H3R/F9iZzVz3kYpS1kH5RC//R/ss9CHXQzwLdWpELEKpkMFetuS2/7wdmdTQTaMPuSTiolrTapUZWXRL55BPm71H1jNoZxjBxo2z5LUpM6TJr1UxLv7nKbdI2xrLCOb2Sbb1vU6b7Avfc9ArtunJhGQv802KYkNVa8q0hs2fuxIyeoIDqUm5YgmuJDKR/own0oajbL0ZawHFrGdZlojXWd44Flm2rLUYDgpPU2tGidUr/qp6Eq/yBPEk1OpJFFvAqyq5T8lIbOpXOqQQsr6pj+3lJ7M0qb6bnHSeT0zpNVC7sDppU6hwxVDgxSxeLTUOsvlt+NBGCFe+c33QRCiBdvzKgTKtoeLM9ao4A+n1QSszqRzadcVktDjZo6K1SljrhvrMxEqiY1FP5cfUjL1yZ5LW9WNVYBiVIJXz3l2HJsJ0M0Uhdk9wFC2KLXjemZjWDepKwo0602oOMBjobgFwvBC7n7yRCHKBHQTg2KBdTtt7BUWAHQQAVJ3DdL8YAAAOAthBAEDVgR0EAFQd2EEAQNWBHQQAVB3YQQBA1Rn9uRl+2n5ysA7r3mPJh8iWgKGepB+9FHobAJRZdbS62u1KoPOiB9lSOTSZMYnK429QZi1YtHQS6T4JirHnOqz7CKvjUb8ZqvlHLwWUWRVQZiWgzHrEGW9enNgGTz1V6QXxRykXMdRpUoHUycIzQ9kS6qmJEO46KsTaN27FFhNHkM3wllal+a0kKnmLIuG0fgl36Ts286vsmSJkkKeCCWXWCEcOoczKZPQEKLPuO3u0n0SupTLBkStnYsd+eKW15jh8WkKH9bofHlhdUZyC+N5JdWFkzUsvCufT9DyXHQHWaGD10MSLSuKd0kZyyNJYeZOXNFJY8Yy02yV5k38JSUcpzBvXAx/rSWtq5khBkVMThhAyBYMyq6rVZN7i2P9NF9YKifIDZdYqUfJ9EmpOuWrpvkL9RmSCRGszQikRxaSfnDqs4ilMz8culSLYKSp4cWdNda8Q8W5YiY8yE4787uaTwGs26VfK94mU9VwoAc7hjCABZVYos1K8UGY9cpRpB6lRRcBKtY0OHAK6IHNP4o+McOlzrKknFk3PdKKOwsqj5hUoO22rsypUv5SPuvbylMdvrrDN7VvKensAlFkJyVh0kBAlZfI9uDRQZlU9n3ElAUan9OdmZHnCqJ9KIyUEVh0imtk6rHy9FatqDwDutewW2etKW99QiN+SoSidWHtVFltt9oN4wmv7Si5oiNLwHrg+mIES2oQyK5RZocx6RCh3fTBcuOl1OrtTU6H6qbUspVe+zJmEXqkxKy+ELL7Yy0A0mNX0x16OUbGZxR21kKQeXFDH+kSdRPjz6GsmKjNRboshNwT1sZ1EuKYTDsWopFBmjVAZsCshXIArWqtEulPZXYhJL+qp/JiasVfuTNK6fqwKjFYMGakcKLMeYSqmu+UYPAAcd8TuQ5k1h8rYQe0ChH4lAJVAu5y29wrSVMwfBACAFNhfDACoOrCDAICqAzsIAKg6sIMAgKoDOwgAqDppO9hQoh1myxoAABxr0nZQdvU+ChJbXOXRfLcUEgAAHGky5sUi6BjbWC4bxW3ZOwAAOB5gfRAAUHUy7CCrv1nyyAzPl7FPGwBw/MjZVyc7E4eQhwMAgCNJ1rx4duHp/IknoYIpAAAcXzLs4OLJieRLcAAA4HiC+yQAgKqTYQf5zYEAAFAJ0nZQ9pPwS2k3oVcKAKgC0GEFAFQdrA8CAKoO7CAAoOrADgIAqg7sIACg6sAOAgCqDuwgAKDqwA4CAKqN5/0/f7oq1zZzYkIAAAAASUVORK5CYII=\" />   </p>  </li>  <li>   <p>Include the resulting <em>token</em> in the <em>Authorization</em> header in the form of a <em>Bearer</em>    (For example, 'Authorization': 'Bearer {TOKEN}') in every request made to the API service</p>  </li>  <li>   <p>Call the <a href=\"#/Session/LoginCloud\">Cloud Login API</a></p>  </li>  <li>   <p>Include the resulting <em>x-mgmt-api-token</em> in Header <em>x-mgmt-api-token</em> of all subsequent    requests</p>  </li> </ol>  # noqa: E501

    The version of the OpenAPI document: 1.9.179
    Contact: harmony-endpoint-external-api@checkpoint.com
    Generated by: https://openapi-generator.tech
"""

from dataclasses import dataclass
from decimal import Decimal
import enum
import email
import json
import os
import io
import atexit
from multiprocessing.pool import ThreadPool
import re
import tempfile
import typing
import typing_extensions
import urllib3
from urllib3._collections import HTTPHeaderDict
from urllib.parse import urlparse, quote
from urllib3.fields import RequestField as RequestFieldBase

import frozendict

from chkp_harmony_endpoint_management_sdk.generated.cloud import rest
from chkp_harmony_endpoint_management_sdk.generated.cloud.configuration import Configuration
from chkp_harmony_endpoint_management_sdk.generated.cloud.exceptions import ApiTypeError, ApiValueError
from chkp_harmony_endpoint_management_sdk.generated.cloud.schemas import (
    NoneClass,
    BoolClass,
    Schema,
    FileIO,
    BinarySchema,
    date,
    datetime,
    none_type,
    Unset,
    unset,
)


class RequestField(RequestFieldBase):
    def __eq__(self, other):
        if not isinstance(other, RequestField):
            return False
        return self.__dict__ == other.__dict__


class JSONEncoder(json.JSONEncoder):
    compact_separators = (',', ':')

    def default(self, obj):
        if isinstance(obj, str):
            return str(obj)
        elif isinstance(obj, float):
            return float(obj)
        elif isinstance(obj, int):
            return int(obj)
        elif isinstance(obj, Decimal):
            if obj.as_tuple().exponent >= 0:
                return int(obj)
            return float(obj)
        elif isinstance(obj, NoneClass):
            return None
        elif isinstance(obj, BoolClass):
            return bool(obj)
        elif isinstance(obj, (dict, frozendict.frozendict)):
            return {key: self.default(val) for key, val in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self.default(item) for item in obj]
        raise ApiValueError('Unable to prepare type {} for serialization'.format(obj.__class__.__name__))


class ParameterInType(enum.Enum):
    QUERY = 'query'
    HEADER = 'header'
    PATH = 'path'
    COOKIE = 'cookie'


class ParameterStyle(enum.Enum):
    MATRIX = 'matrix'
    LABEL = 'label'
    FORM = 'form'
    SIMPLE = 'simple'
    SPACE_DELIMITED = 'spaceDelimited'
    PIPE_DELIMITED = 'pipeDelimited'
    DEEP_OBJECT = 'deepObject'


class PrefixSeparatorIterator:
    # A class to store prefixes and separators for rfc6570 expansions

    def __init__(self, prefix: str, separator: str):
        self.prefix = prefix
        self.separator = separator
        self.first = True
        if separator in {'.', '|', '%20'}:
            item_separator = separator
        else:
            item_separator = ','
        self.item_separator = item_separator

    def __iter__(self):
        return self

    def __next__(self):
        if self.first:
            self.first = False
            return self.prefix
        return self.separator


class ParameterSerializerBase:
    @classmethod
    def _get_default_explode(cls, style: ParameterStyle) -> bool:
        return False

    @staticmethod
    def __ref6570_item_value(in_data: typing.Any, percent_encode: bool):
        """
        Get representation if str/float/int/None/items in list/ values in dict
        None is returned if an item is undefined, use cases are value=
        - None
        - []
        - {}
        - [None, None None]
        - {'a': None, 'b': None}
        """
        if type(in_data) in {str, float, int}:
            if percent_encode:
                return quote(str(in_data))
            return str(in_data)
        elif isinstance(in_data, none_type):
            # ignored by the expansion process https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.1
            return None
        elif isinstance(in_data, list) and not in_data:
            # ignored by the expansion process https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.1
            return None
        elif isinstance(in_data, dict) and not in_data:
            # ignored by the expansion process https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.1
            return None
        raise ApiValueError('Unable to generate a ref6570 item representation of {}'.format(in_data))

    @staticmethod
    def _to_dict(name: str, value: str):
        return {name: value}

    @classmethod
    def __ref6570_str_float_int_expansion(
        cls,
        variable_name: str,
        in_data: typing.Any,
        explode: bool,
        percent_encode: bool,
        prefix_separator_iterator: PrefixSeparatorIterator,
        var_name_piece: str,
        named_parameter_expansion: bool
    ) -> str:
        item_value = cls.__ref6570_item_value(in_data, percent_encode)
        if item_value is None or (item_value == '' and prefix_separator_iterator.separator == ';'):
            return next(prefix_separator_iterator) + var_name_piece
        value_pair_equals = '=' if named_parameter_expansion else ''
        return next(prefix_separator_iterator) + var_name_piece + value_pair_equals + item_value

    @classmethod
    def __ref6570_list_expansion(
        cls,
        variable_name: str,
        in_data: typing.Any,
        explode: bool,
        percent_encode: bool,
        prefix_separator_iterator: PrefixSeparatorIterator,
        var_name_piece: str,
        named_parameter_expansion: bool
    ) -> str:
        item_values = [cls.__ref6570_item_value(v, percent_encode) for v in in_data]
        item_values = [v for v in item_values if v is not None]
        if not item_values:
            # ignored by the expansion process https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.1
            return ""
        value_pair_equals = '=' if named_parameter_expansion else ''
        if not explode:
            return (
                next(prefix_separator_iterator) +
                var_name_piece +
                value_pair_equals +
                prefix_separator_iterator.item_separator.join(item_values)
            )
        # exploded
        return next(prefix_separator_iterator) + next(prefix_separator_iterator).join(
            [var_name_piece + value_pair_equals + val for val in item_values]
        )

    @classmethod
    def __ref6570_dict_expansion(
        cls,
        variable_name: str,
        in_data: typing.Any,
        explode: bool,
        percent_encode: bool,
        prefix_separator_iterator: PrefixSeparatorIterator,
        var_name_piece: str,
        named_parameter_expansion: bool
    ) -> str:
        in_data_transformed = {key: cls.__ref6570_item_value(val, percent_encode) for key, val in in_data.items()}
        in_data_transformed = {key: val for key, val in in_data_transformed.items() if val is not None}
        if not in_data_transformed:
            # ignored by the expansion process https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.1
            return ""
        value_pair_equals = '=' if named_parameter_expansion else ''
        if not explode:
            return (
                next(prefix_separator_iterator) +
                var_name_piece + value_pair_equals +
                prefix_separator_iterator.item_separator.join(
                    prefix_separator_iterator.item_separator.join(
                        item_pair
                    ) for item_pair in in_data_transformed.items()
                )
            )
        # exploded
        return next(prefix_separator_iterator) + next(prefix_separator_iterator).join(
            [key + '=' + val for key, val in in_data_transformed.items()]
        )

    @classmethod
    def _ref6570_expansion(
        cls,
        variable_name: str,
        in_data: typing.Any,
        explode: bool,
        percent_encode: bool,
        prefix_separator_iterator: PrefixSeparatorIterator
    ) -> str:
        """
        Separator is for separate variables like dict with explode true, not for array item separation
        """
        named_parameter_expansion = prefix_separator_iterator.separator in {'&', ';'}
        var_name_piece = variable_name if named_parameter_expansion else ''
        if type(in_data) in {str, float, int}:
            return cls.__ref6570_str_float_int_expansion(
                variable_name,
                in_data,
                explode,
                percent_encode,
                prefix_separator_iterator,
                var_name_piece,
                named_parameter_expansion
            )
        elif isinstance(in_data, none_type):
            # ignored by the expansion process https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.1
            return ""
        elif isinstance(in_data, list):
            return cls.__ref6570_list_expansion(
                variable_name,
                in_data,
                explode,
                percent_encode,
                prefix_separator_iterator,
                var_name_piece,
                named_parameter_expansion
            )
        elif isinstance(in_data, dict):
            return cls.__ref6570_dict_expansion(
                variable_name,
                in_data,
                explode,
                percent_encode,
                prefix_separator_iterator,
                var_name_piece,
                named_parameter_expansion
            )
        # bool, bytes, etc
        raise ApiValueError('Unable to generate a ref6570 representation of {}'.format(in_data))


class StyleFormSerializer(ParameterSerializerBase):
    @classmethod
    def _get_default_explode(cls, style: ParameterStyle) -> bool:
        if style is ParameterStyle.FORM:
            return True
        return super()._get_default_explode(style)

    def _serialize_form(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list],
        name: str,
        explode: bool,
        percent_encode: bool,
        prefix_separator_iterator: typing.Optional[PrefixSeparatorIterator] = None
    ) -> str:
        if prefix_separator_iterator is None:
            prefix_separator_iterator = PrefixSeparatorIterator('', '&')
        return self._ref6570_expansion(
            variable_name=name,
            in_data=in_data,
            explode=explode,
            percent_encode=percent_encode,
            prefix_separator_iterator=prefix_separator_iterator
        )


class StyleSimpleSerializer(ParameterSerializerBase):

    def _serialize_simple(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list],
        name: str,
        explode: bool,
        percent_encode: bool
    ) -> str:
        prefix_separator_iterator = PrefixSeparatorIterator('', ',')
        return self._ref6570_expansion(
            variable_name=name,
            in_data=in_data,
            explode=explode,
            percent_encode=percent_encode,
            prefix_separator_iterator=prefix_separator_iterator
        )


class JSONDetector:
    """
    Works for:
    application/json
    application/json; charset=UTF-8
    application/json-patch+json
    application/geo+json
    """
    __json_content_type_pattern = re.compile("application/[^+]*[+]?(json);?.*")

    @classmethod
    def _content_type_is_json(cls, content_type: str) -> bool:
        if cls.__json_content_type_pattern.match(content_type):
            return True
        return False


@dataclass
class ParameterBase(JSONDetector):
    name: str
    in_type: ParameterInType
    required: bool
    style: typing.Optional[ParameterStyle]
    explode: typing.Optional[bool]
    allow_reserved: typing.Optional[bool]
    schema: typing.Optional[typing.Type[Schema]]
    content: typing.Optional[typing.Dict[str, typing.Type[Schema]]]

    __style_to_in_type = {
        ParameterStyle.MATRIX: {ParameterInType.PATH},
        ParameterStyle.LABEL: {ParameterInType.PATH},
        ParameterStyle.FORM: {ParameterInType.QUERY, ParameterInType.COOKIE},
        ParameterStyle.SIMPLE: {ParameterInType.PATH, ParameterInType.HEADER},
        ParameterStyle.SPACE_DELIMITED: {ParameterInType.QUERY},
        ParameterStyle.PIPE_DELIMITED: {ParameterInType.QUERY},
        ParameterStyle.DEEP_OBJECT: {ParameterInType.QUERY},
    }
    __in_type_to_default_style = {
        ParameterInType.QUERY: ParameterStyle.FORM,
        ParameterInType.PATH: ParameterStyle.SIMPLE,
        ParameterInType.HEADER: ParameterStyle.SIMPLE,
        ParameterInType.COOKIE: ParameterStyle.FORM,
    }
    __disallowed_header_names = {'Accept', 'Content-Type', 'Authorization'}
    _json_encoder = JSONEncoder()

    @classmethod
    def __verify_style_to_in_type(cls, style: typing.Optional[ParameterStyle], in_type: ParameterInType):
        if style is None:
            return
        in_type_set = cls.__style_to_in_type[style]
        if in_type not in in_type_set:
            raise ValueError(
                'Invalid style and in_type combination. For style={} only in_type={} are allowed'.format(
                    style, in_type_set
                )
            )

    def __init__(
        self,
        name: str,
        in_type: ParameterInType,
        required: bool = False,
        style: typing.Optional[ParameterStyle] = None,
        explode: bool = False,
        allow_reserved: typing.Optional[bool] = None,
        schema: typing.Optional[typing.Type[Schema]] = None,
        content: typing.Optional[typing.Dict[str, typing.Type[Schema]]] = None
    ):
        if schema is None and content is None:
            raise ValueError('Value missing; Pass in either schema or content')
        if schema and content:
            raise ValueError('Too many values provided. Both schema and content were provided. Only one may be input')
        if name in self.__disallowed_header_names and in_type is ParameterInType.HEADER:
            raise ValueError('Invalid name, name may not be one of {}'.format(self.__disallowed_header_names))
        self.__verify_style_to_in_type(style, in_type)
        if content is None and style is None:
            style = self.__in_type_to_default_style[in_type]
        if content is not None and in_type in self.__in_type_to_default_style and len(content) != 1:
            raise ValueError('Invalid content length, content length must equal 1')
        self.in_type = in_type
        self.name = name
        self.required = required
        self.style = style
        self.explode = explode
        self.allow_reserved = allow_reserved
        self.schema = schema
        self.content = content

    def _serialize_json(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list],
        eliminate_whitespace: bool = False
    ) -> str:
        if eliminate_whitespace:
            return json.dumps(in_data, separators=self._json_encoder.compact_separators)
        return json.dumps(in_data)


class PathParameter(ParameterBase, StyleSimpleSerializer):

    def __init__(
        self,
        name: str,
        required: bool = False,
        style: typing.Optional[ParameterStyle] = None,
        explode: bool = False,
        allow_reserved: typing.Optional[bool] = None,
        schema: typing.Optional[typing.Type[Schema]] = None,
        content: typing.Optional[typing.Dict[str, typing.Type[Schema]]] = None
    ):
        super().__init__(
            name,
            in_type=ParameterInType.PATH,
            required=required,
            style=style,
            explode=explode,
            allow_reserved=allow_reserved,
            schema=schema,
            content=content
        )

    def __serialize_label(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list]
    ) -> typing.Dict[str, str]:
        prefix_separator_iterator = PrefixSeparatorIterator('.', '.')
        value = self._ref6570_expansion(
            variable_name=self.name,
            in_data=in_data,
            explode=self.explode,
            percent_encode=True,
            prefix_separator_iterator=prefix_separator_iterator
        )
        return self._to_dict(self.name, value)

    def __serialize_matrix(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list]
    ) -> typing.Dict[str, str]:
        prefix_separator_iterator = PrefixSeparatorIterator(';', ';')
        value = self._ref6570_expansion(
            variable_name=self.name,
            in_data=in_data,
            explode=self.explode,
            percent_encode=True,
            prefix_separator_iterator=prefix_separator_iterator
        )
        return self._to_dict(self.name, value)

    def __serialize_simple(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list],
    ) -> typing.Dict[str, str]:
        value = self._serialize_simple(
            in_data=in_data,
            name=self.name,
            explode=self.explode,
            percent_encode=True
        )
        return self._to_dict(self.name, value)

    def serialize(
        self,
        in_data: typing.Union[
            Schema, Decimal, int, float, str, date, datetime, None, bool, list, tuple, dict, frozendict.frozendict]
    ) -> typing.Dict[str, str]:
        if self.schema:
            cast_in_data = self.schema(in_data)
            cast_in_data = self._json_encoder.default(cast_in_data)
            """
            simple -> path
                path:
                    returns path_params: dict
            label -> path
                returns path_params
            matrix -> path
                returns path_params
            """
            if self.style:
                if self.style is ParameterStyle.SIMPLE:
                    return self.__serialize_simple(cast_in_data)
                elif self.style is ParameterStyle.LABEL:
                    return self.__serialize_label(cast_in_data)
                elif self.style is ParameterStyle.MATRIX:
                    return self.__serialize_matrix(cast_in_data)
        # self.content will be length one
        for content_type, schema in self.content.items():
            cast_in_data = schema(in_data)
            cast_in_data = self._json_encoder.default(cast_in_data)
            if self._content_type_is_json(content_type):
                value = self._serialize_json(cast_in_data)
                return self._to_dict(self.name, value)
            raise NotImplementedError('Serialization of {} has not yet been implemented'.format(content_type))


class QueryParameter(ParameterBase, StyleFormSerializer):

    def __init__(
        self,
        name: str,
        required: bool = False,
        style: typing.Optional[ParameterStyle] = None,
        explode: typing.Optional[bool] = None,
        allow_reserved: typing.Optional[bool] = None,
        schema: typing.Optional[typing.Type[Schema]] = None,
        content: typing.Optional[typing.Dict[str, typing.Type[Schema]]] = None
    ):
        used_style = ParameterStyle.FORM if style is None else style
        used_explode = self._get_default_explode(used_style) if explode is None else explode

        super().__init__(
            name,
            in_type=ParameterInType.QUERY,
            required=required,
            style=used_style,
            explode=used_explode,
            allow_reserved=allow_reserved,
            schema=schema,
            content=content
        )

    def __serialize_space_delimited(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list],
        prefix_separator_iterator: typing.Optional[PrefixSeparatorIterator]
    ) -> typing.Dict[str, str]:
        if prefix_separator_iterator is None:
            prefix_separator_iterator = self.get_prefix_separator_iterator()
        value = self._ref6570_expansion(
            variable_name=self.name,
            in_data=in_data,
            explode=self.explode,
            percent_encode=True,
            prefix_separator_iterator=prefix_separator_iterator
        )
        return self._to_dict(self.name, value)

    def __serialize_pipe_delimited(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list],
        prefix_separator_iterator: typing.Optional[PrefixSeparatorIterator]
    ) -> typing.Dict[str, str]:
        if prefix_separator_iterator is None:
            prefix_separator_iterator = self.get_prefix_separator_iterator()
        value = self._ref6570_expansion(
            variable_name=self.name,
            in_data=in_data,
            explode=self.explode,
            percent_encode=True,
            prefix_separator_iterator=prefix_separator_iterator
        )
        return self._to_dict(self.name, value)

    def __serialize_form(
        self,
        in_data: typing.Union[None, int, float, str, bool, dict, list],
        prefix_separator_iterator: typing.Optional[PrefixSeparatorIterator]
    ) -> typing.Dict[str, str]:
        if prefix_separator_iterator is None:
            prefix_separator_iterator = self.get_prefix_separator_iterator()
        value = self._serialize_form(
            in_data,
            name=self.name,
            explode=self.explode,
            percent_encode=True,
            prefix_separator_iterator=prefix_separator_iterator
        )
        return self._to_dict(self.name, value)

    def get_prefix_separator_iterator(self) -> typing.Optional[PrefixSeparatorIterator]:
        if self.style is ParameterStyle.FORM:
            return PrefixSeparatorIterator('?', '&')
        elif self.style is ParameterStyle.SPACE_DELIMITED:
            return PrefixSeparatorIterator('', '%20')
        elif self.style is ParameterStyle.PIPE_DELIMITED:
            return PrefixSeparatorIterator('', '|')

    def serialize(
        self,
        in_data: typing.Union[
            Schema, Decimal, int, float, str, date, datetime, None, bool, list, tuple, dict, frozendict.frozendict],
        prefix_separator_iterator: typing.Optional[PrefixSeparatorIterator] = None
    ) -> typing.Dict[str, str]:
        if self.schema:
            cast_in_data = self.schema(in_data)
            cast_in_data = self._json_encoder.default(cast_in_data)
            """
            form -> query
                query:
                    - GET/HEAD/DELETE: could use fields
                    - PUT/POST: must use urlencode to send parameters
                    returns fields: tuple
            spaceDelimited -> query
                returns fields
            pipeDelimited -> query
                returns fields
            deepObject -> query, https://github.com/OAI/OpenAPI-Specification/issues/1706
                returns fields
            """
            if self.style:
                # TODO update query ones to omit setting values when [] {} or None is input
                if self.style is ParameterStyle.FORM:
                    return self.__serialize_form(cast_in_data, prefix_separator_iterator)
                elif self.style is ParameterStyle.SPACE_DELIMITED:
                    return self.__serialize_space_delimited(cast_in_data, prefix_separator_iterator)
                elif self.style is ParameterStyle.PIPE_DELIMITED:
                    return self.__serialize_pipe_delimited(cast_in_data, prefix_separator_iterator)
        # self.content will be length one
        if prefix_separator_iterator is None:
            prefix_separator_iterator = self.get_prefix_separator_iterator()
        for content_type, schema in self.content.items():
            cast_in_data = schema(in_data)
            cast_in_data = self._json_encoder.default(cast_in_data)
            if self._content_type_is_json(content_type):
                value = self._serialize_json(cast_in_data, eliminate_whitespace=True)
                return self._to_dict(
                    self.name,
                    next(prefix_separator_iterator) + self.name + '=' + quote(value)
                )
            raise NotImplementedError('Serialization of {} has not yet been implemented'.format(content_type))


class CookieParameter(ParameterBase, StyleFormSerializer):

    def __init__(
        self,
        name: str,
        required: bool = False,
        style: typing.Optional[ParameterStyle] = None,
        explode: typing.Optional[bool] = None,
        allow_reserved: typing.Optional[bool] = None,
        schema: typing.Optional[typing.Type[Schema]] = None,
        content: typing.Optional[typing.Dict[str, typing.Type[Schema]]] = None
    ):
        used_style = ParameterStyle.FORM if style is None and content is None and schema else style
        used_explode = self._get_default_explode(used_style) if explode is None else explode

        super().__init__(
            name,
            in_type=ParameterInType.COOKIE,
            required=required,
            style=used_style,
            explode=used_explode,
            allow_reserved=allow_reserved,
            schema=schema,
            content=content
        )

    def serialize(
        self,
        in_data: typing.Union[
            Schema, Decimal, int, float, str, date, datetime, None, bool, list, tuple, dict, frozendict.frozendict]
    ) -> typing.Dict[str, str]:
        if self.schema:
            cast_in_data = self.schema(in_data)
            cast_in_data = self._json_encoder.default(cast_in_data)
            """
            form -> cookie
                returns fields: tuple
            """
            if self.style:
                """
                TODO add escaping of comma, space, equals
                or turn encoding on
                """
                value = self._serialize_form(
                    cast_in_data,
                    explode=self.explode,
                    name=self.name,
                    percent_encode=False,
                    prefix_separator_iterator=PrefixSeparatorIterator('', '&')
                )
                return self._to_dict(self.name, value)
        # self.content will be length one
        for content_type, schema in self.content.items():
            cast_in_data = schema(in_data)
            cast_in_data = self._json_encoder.default(cast_in_data)
            if self._content_type_is_json(content_type):
                value = self._serialize_json(cast_in_data)
                return self._to_dict(self.name, value)
            raise NotImplementedError('Serialization of {} has not yet been implemented'.format(content_type))


class HeaderParameter(ParameterBase, StyleSimpleSerializer):
    def __init__(
        self,
        name: str,
        required: bool = False,
        style: typing.Optional[ParameterStyle] = None,
        explode: bool = False,
        allow_reserved: typing.Optional[bool] = None,
        schema: typing.Optional[typing.Type[Schema]] = None,
        content: typing.Optional[typing.Dict[str, typing.Type[Schema]]] = None
    ):
        super().__init__(
            name,
            in_type=ParameterInType.HEADER,
            required=required,
            style=style,
            explode=explode,
            allow_reserved=allow_reserved,
            schema=schema,
            content=content
        )

    @staticmethod
    def __to_headers(in_data: typing.Tuple[typing.Tuple[str, str], ...]) -> HTTPHeaderDict:
        data = tuple(t for t in in_data if t)
        headers = HTTPHeaderDict()
        if not data:
            return headers
        headers.extend(data)
        return headers

    def serialize(
        self,
        in_data: typing.Union[
            Schema, Decimal, int, float, str, date, datetime, None, bool, list, tuple, dict, frozendict.frozendict]
    ) -> HTTPHeaderDict:
        if self.schema:
            cast_in_data = self.schema(in_data)
            cast_in_data = self._json_encoder.default(cast_in_data)
            """
            simple -> header
                headers: PoolManager needs a mapping, tuple is close
                    returns headers: dict
            """
            if self.style:
                value = self._serialize_simple(cast_in_data, self.name, self.explode, False)
                return self.__to_headers(((self.name, value),))
        # self.content will be length one
        for content_type, schema in self.content.items():
            cast_in_data = schema(in_data)
            cast_in_data = self._json_encoder.default(cast_in_data)
            if self._content_type_is_json(content_type):
                value = self._serialize_json(cast_in_data)
                return self.__to_headers(((self.name, value),))
            raise NotImplementedError('Serialization of {} has not yet been implemented'.format(content_type))


class Encoding:
    def __init__(
        self,
        content_type: str,
        headers: typing.Optional[typing.Dict[str, HeaderParameter]] = None,
        style: typing.Optional[ParameterStyle] = None,
        explode: bool = False,
        allow_reserved: bool = False,
    ):
        self.content_type = content_type
        self.headers = headers
        self.style = style
        self.explode = explode
        self.allow_reserved = allow_reserved


@dataclass
class MediaType:
    """
    Used to store request and response body schema information
    encoding:
        A map between a property name and its encoding information.
        The key, being the property name, MUST exist in the schema as a property.
        The encoding object SHALL only apply to requestBody objects when the media type is
        multipart or application/x-www-form-urlencoded.
    """
    schema: typing.Optional[typing.Type[Schema]] = None
    encoding: typing.Optional[typing.Dict[str, Encoding]] = None


@dataclass
class ApiResponse:
    response: urllib3.HTTPResponse
    body: typing.Union[Unset, Schema] = unset
    headers: typing.Union[Unset, typing.Dict[str, Schema]] = unset

    def __init__(
        self,
        response: urllib3.HTTPResponse,
        body: typing.Union[Unset, Schema] = unset,
        headers: typing.Union[Unset, typing.Dict[str, Schema]] = unset
    ):
        """
        pycharm needs this to prevent 'Unexpected argument' warnings
        """
        self.response = response
        self.body = body
        self.headers = headers


@dataclass
class ApiResponseWithoutDeserialization(ApiResponse):
    response: urllib3.HTTPResponse
    body: typing.Union[Unset, typing.Type[Schema]] = unset
    headers: typing.Union[Unset, typing.List[HeaderParameter]] = unset


class OpenApiResponse(JSONDetector):
    __filename_content_disposition_pattern = re.compile('filename="(.+?)"')

    def __init__(
        self,
        response_cls: typing.Type[ApiResponse] = ApiResponse,
        content: typing.Optional[typing.Dict[str, MediaType]] = None,
        headers: typing.Optional[typing.List[HeaderParameter]] = None,
    ):
        self.headers = headers
        if content is not None and len(content) == 0:
            raise ValueError('Invalid value for content, the content dict must have >= 1 entry')
        self.content = content
        self.response_cls = response_cls

    @staticmethod
    def __deserialize_json(response: urllib3.HTTPResponse) -> typing.Any:
        # python must be >= 3.9 so we can pass in bytes into json.loads
        return json.loads(response.data)

    @staticmethod
    def __file_name_from_response_url(response_url: typing.Optional[str]) -> typing.Optional[str]:
        if response_url is None:
            return None
        url_path = urlparse(response_url).path
        if url_path:
            path_basename = os.path.basename(url_path)
            if path_basename:
                _filename, ext = os.path.splitext(path_basename)
                if ext:
                    return path_basename
        return None

    @classmethod
    def __file_name_from_content_disposition(cls, content_disposition: typing.Optional[str]) -> typing.Optional[str]:
        if content_disposition is None:
            return None
        match = cls.__filename_content_disposition_pattern.search(content_disposition)
        if not match:
            return None
        return match.group(1)

    def __deserialize_application_octet_stream(
        self, response: urllib3.HTTPResponse
    ) -> typing.Union[bytes, io.BufferedReader]:
        """
        urllib3 use cases:
        1. when preload_content=True (stream=False) then supports_chunked_reads is False and bytes are returned
        2. when preload_content=False (stream=True) then supports_chunked_reads is True and
            a file will be written and returned
        """
        if response.supports_chunked_reads():
            file_name = (
                self.__file_name_from_content_disposition(response.headers.get('content-disposition'))
                or self.__file_name_from_response_url(response.geturl())
            )

            if file_name is None:
                _fd, path = tempfile.mkstemp()
            else:
                path = os.path.join(tempfile.gettempdir(), file_name)

            with open(path, 'wb') as new_file:
                chunk_size = 1024
                while True:
                    data = response.read(chunk_size)
                    if not data:
                        break
                    new_file.write(data)
            # release_conn is needed for streaming connections only
            response.release_conn()
            new_file = open(path, 'rb')
            return new_file
        else:
            return response.data

    @staticmethod
    def __deserialize_multipart_form_data(
        response: urllib3.HTTPResponse
    ) -> typing.Dict[str, typing.Any]:
        msg = email.message_from_bytes(response.data)
        return {
            part.get_param("name", header="Content-Disposition"): part.get_payload(
                decode=True
            ).decode(part.get_content_charset())
            if part.get_content_charset()
            else part.get_payload()
            for part in msg.get_payload()
        }

    def deserialize(self, response: urllib3.HTTPResponse, configuration: Configuration) -> ApiResponse:
        content_type = response.getheader('content-type')
        deserialized_body = unset
        streamed = response.supports_chunked_reads()

        deserialized_headers = unset
        if self.headers is not None:
            # TODO add header deserialiation here
            pass

        if self.content is not None:
            if content_type not in self.content:
                raise ApiValueError(
                    f"Invalid content_type returned. Content_type='{content_type}' was returned "
                    f"when only {str(set(self.content))} are defined for status_code={str(response.status)}"
                )
            body_schema = self.content[content_type].schema
            if body_schema is None:
                # some specs do not define response content media type schemas
                return self.response_cls(
                    response=response,
                    headers=deserialized_headers,
                    body=unset
                )

            if self._content_type_is_json(content_type):
                body_data = self.__deserialize_json(response)
            elif content_type == 'application/octet-stream':
                body_data = self.__deserialize_application_octet_stream(response)
            elif content_type.startswith('multipart/form-data'):
                body_data = self.__deserialize_multipart_form_data(response)
                content_type = 'multipart/form-data'
            else:
                raise NotImplementedError('Deserialization of {} has not yet been implemented'.format(content_type))
            deserialized_body = body_schema.from_openapi_data_oapg(
                body_data, _configuration=configuration)
        elif streamed:
            response.release_conn()

        return self.response_cls(
            response=response,
            headers=deserialized_headers,
            body=deserialized_body
        )


class ApiClient:
    """Generic API client for OpenAPI client library builds.

    OpenAPI generic API client. This client handles the client-
    server communication, and is invariant across implementations. Specifics of
    the methods and models for each application are generated from the OpenAPI
    templates.

    NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech
    Do not edit the class manually.

    :param configuration: .Configuration object for this client
    :param header_name: a header to pass when making calls to the API.
    :param header_value: a header value to pass when making calls to
        the API.
    :param cookie: a cookie to include in the header when making calls
        to the API
    :param pool_threads: The number of threads to use for async requests
        to the API. More threads means more concurrent API requests.
    """

    _pool = None

    def __init__(
        self,
        configuration: typing.Optional[Configuration] = None,
        header_name: typing.Optional[str] = None,
        header_value: typing.Optional[str] = None,
        cookie: typing.Optional[str] = None,
        pool_threads: int = 1
    ):
        if configuration is None:
            configuration = Configuration()
        self.configuration = configuration
        self.pool_threads = pool_threads

        self.rest_client = rest.RESTClientObject(configuration)
        self.default_headers = HTTPHeaderDict()
        if header_name is not None:
            self.default_headers[header_name] = header_value
        self.cookie = cookie
        # Set default User-Agent.
        self.user_agent = 'OpenAPI-Generator/1.0.0/python'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        if self._pool:
            self._pool.close()
            self._pool.join()
            self._pool = None
            if hasattr(atexit, 'unregister'):
                atexit.unregister(self.close)

    @property
    def pool(self):
        """Create thread pool on first request
         avoids instantiating unused threadpool for blocking clients.
        """
        if self._pool is None:
            atexit.register(self.close)
            self._pool = ThreadPool(self.pool_threads)
        return self._pool

    @property
    def user_agent(self):
        """User agent for this API client"""
        return self.default_headers['User-Agent']

    @user_agent.setter
    def user_agent(self, value):
        self.default_headers['User-Agent'] = value

    def set_default_header(self, header_name, header_value):
        self.default_headers[header_name] = header_value

    def __call_api(
        self,
        resource_path: str,
        method: str,
        headers: typing.Optional[HTTPHeaderDict] = None,
        body: typing.Optional[typing.Union[str, bytes]] = None,
        fields: typing.Optional[typing.Tuple[typing.Tuple[str, str], ...]] = None,
        auth_settings: typing.Optional[typing.List[str]] = None,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        host: typing.Optional[str] = None,
    ) -> urllib3.HTTPResponse:

        # header parameters
        used_headers = HTTPHeaderDict(self.default_headers)
        if self.cookie:
            headers['Cookie'] = self.cookie

        # auth setting
        self.update_params_for_auth(used_headers,
                                    auth_settings, resource_path, method, body)

        # must happen after cookie setting and auth setting in case user is overriding those
        if headers:
            used_headers.update(headers)

        # request url
        if host is None:
            url = self.configuration.host + resource_path
        else:
            # use server/host defined in path or operation instead
            url = host + resource_path

        # perform request and return response
        response = self.request(
            method,
            url,
            headers=used_headers,
            fields=fields,
            body=body,
            stream=stream,
            timeout=timeout,
        )
        return response

    def call_api(
        self,
        resource_path: str,
        method: str,
        headers: typing.Optional[HTTPHeaderDict] = None,
        body: typing.Optional[typing.Union[str, bytes]] = None,
        fields: typing.Optional[typing.Tuple[typing.Tuple[str, str], ...]] = None,
        auth_settings: typing.Optional[typing.List[str]] = None,
        async_req: typing.Optional[bool] = None,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        host: typing.Optional[str] = None,
    ) -> urllib3.HTTPResponse:
        """Makes the HTTP request (synchronous) and returns deserialized data.

        To make an async_req request, set the async_req parameter.

        :param resource_path: Path to method endpoint.
        :param method: Method to call.
        :param headers: Header parameters to be
            placed in the request header.
        :param body: Request body.
        :param fields: Request post form parameters,
            for `application/x-www-form-urlencoded`, `multipart/form-data`.
        :param auth_settings: Auth Settings names for the request.
        :param async_req: execute request asynchronously
        :type async_req: bool, optional TODO remove, unused
        :param stream: if True, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Also when True, if the openapi spec describes a file download,
                                 the data will be written to a local filesystme file and the BinarySchema
                                 instance will also inherit from FileSchema and FileIO
                                 Default is False.
        :type stream: bool, optional
        :param timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param host: api endpoint host
        :return:
            If async_req parameter is True,
            the request will be called asynchronously.
            The method will return the request thread.
            If parameter async_req is False or missing,
            then the method will return the response directly.
        """

        if not async_req:
            return self.__call_api(
                resource_path,
                method,
                headers,
                body,
                fields,
                auth_settings,
                stream,
                timeout,
                host,
            )

        return self.pool.apply_async(
            self.__call_api,
            (
                resource_path,
                method,
                headers,
                body,
                json,
                fields,
                auth_settings,
                stream,
                timeout,
                host,
            )
        )

    def request(
        self,
        method: str,
        url: str,
        headers: typing.Optional[HTTPHeaderDict] = None,
        fields: typing.Optional[typing.Tuple[typing.Tuple[str, str], ...]] = None,
        body: typing.Optional[typing.Union[str, bytes]] = None,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
    ) -> urllib3.HTTPResponse:
        """Makes the HTTP request using RESTClient."""
        if method == "GET":
            return self.rest_client.GET(url,
                                        stream=stream,
                                        timeout=timeout,
                                        headers=headers)
        elif method == "HEAD":
            return self.rest_client.HEAD(url,
                                         stream=stream,
                                         timeout=timeout,
                                         headers=headers)
        elif method == "OPTIONS":
            return self.rest_client.OPTIONS(url,
                                            headers=headers,
                                            fields=fields,
                                            stream=stream,
                                            timeout=timeout,
                                            body=body)
        elif method == "POST":
            return self.rest_client.POST(url,
                                         headers=headers,
                                         fields=fields,
                                         stream=stream,
                                         timeout=timeout,
                                         body=body)
        elif method == "PUT":
            return self.rest_client.PUT(url,
                                        headers=headers,
                                        fields=fields,
                                        stream=stream,
                                        timeout=timeout,
                                        body=body)
        elif method == "PATCH":
            return self.rest_client.PATCH(url,
                                          headers=headers,
                                          fields=fields,
                                          stream=stream,
                                          timeout=timeout,
                                          body=body)
        elif method == "DELETE":
            return self.rest_client.DELETE(url,
                                           headers=headers,
                                           stream=stream,
                                           timeout=timeout,
                                           body=body)
        else:
            raise ApiValueError(
                "http method must be `GET`, `HEAD`, `OPTIONS`,"
                " `POST`, `PATCH`, `PUT` or `DELETE`."
            )

    def update_params_for_auth(self, headers, auth_settings,
                               resource_path, method, body):
        """Updates header and query params based on authentication setting.

        :param headers: Header parameters dict to be updated.
        :param auth_settings: Authentication setting identifiers list.
        :param resource_path: A string representation of the HTTP request resource path.
        :param method: A string representation of the HTTP request method.
        :param body: A object representing the body of the HTTP request.
            The object type is the return value of _encoder.default().
        """
        if not auth_settings:
            return

        for auth in auth_settings:
            auth_setting = self.configuration.auth_settings().get(auth)
            if not auth_setting:
                continue
            if auth_setting['in'] == 'cookie':
                headers.add('Cookie', auth_setting['value'])
            elif auth_setting['in'] == 'header':
                if auth_setting['type'] != 'http-signature':
                    headers.add(auth_setting['key'], auth_setting['value'])
            elif auth_setting['in'] == 'query':
                """ TODO implement auth in query
                need to pass in prefix_separator_iterator
                and need to output resource_path with query params added
                """
                raise ApiValueError("Auth in query not yet implemented")
            else:
                raise ApiValueError(
                    'Authentication token must be in `query` or `header`'
                )


class Api:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client: typing.Optional[ApiClient] = None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    @staticmethod
    def _verify_typed_dict_inputs_oapg(cls: typing.Type[typing_extensions.TypedDict], data: typing.Dict[str, typing.Any]):
        """
        Ensures that:
        - required keys are present
        - additional properties are not input
        - value stored under required keys do not have the value unset
        Note: detailed value checking is done in schema classes
        """
        missing_required_keys = []
        required_keys_with_unset_values = []
        for required_key in cls.__required_keys__:
            if required_key not in data:
                missing_required_keys.append(required_key)
                continue
            value = data[required_key]
            if value is unset:
                required_keys_with_unset_values.append(required_key)
        if missing_required_keys:
            raise ApiTypeError(
                '{} missing {} required arguments: {}'.format(
                    cls.__name__, len(missing_required_keys), missing_required_keys
                 )
             )
        if required_keys_with_unset_values:
            raise ApiValueError(
                '{} contains invalid unset values for {} required keys: {}'.format(
                    cls.__name__, len(required_keys_with_unset_values), required_keys_with_unset_values
                )
            )

        disallowed_additional_keys = []
        for key in data:
            if key in cls.__required_keys__ or key in cls.__optional_keys__:
                continue
            disallowed_additional_keys.append(key)
        if disallowed_additional_keys:
            raise ApiTypeError(
                '{} got {} unexpected keyword arguments: {}'.format(
                    cls.__name__, len(disallowed_additional_keys), disallowed_additional_keys
                )
            )

    def _get_host_oapg(
        self,
        operation_id: str,
        servers: typing.Tuple[typing.Dict[str, str], ...] = tuple(),
        host_index: typing.Optional[int] = None
    ) -> typing.Optional[str]:
        configuration = self.api_client.configuration
        try:
            if host_index is None:
                index = configuration.server_operation_index.get(
                    operation_id, configuration.server_index
                )
            else:
                index = host_index
            server_variables = configuration.server_operation_variables.get(
                operation_id, configuration.server_variables
            )
            host = configuration.get_host_from_settings(
                index, variables=server_variables, servers=servers
            )
        except IndexError:
            if servers:
                raise ApiValueError(
                    "Invalid host index. Must be 0 <= index < %s" %
                    len(servers)
                )
            host = None
        return host


class SerializedRequestBody(typing_extensions.TypedDict, total=False):
    body: typing.Union[str, bytes]
    fields: typing.Tuple[typing.Union[RequestField, typing.Tuple[str, str]], ...]


class RequestBody(StyleFormSerializer, JSONDetector):
    """
    A request body parameter
    content: content_type to MediaType Schema info
    """
    __json_encoder = JSONEncoder()

    def __init__(
        self,
        content: typing.Dict[str, MediaType],
        required: bool = False,
    ):
        self.required = required
        if len(content) == 0:
            raise ValueError('Invalid value for content, the content dict must have >= 1 entry')
        self.content = content

    def __serialize_json(
        self,
        in_data: typing.Any
    ) -> typing.Dict[str, bytes]:
        in_data = self.__json_encoder.default(in_data)
        json_str = json.dumps(in_data, separators=(",", ":"), ensure_ascii=False).encode(
            "utf-8"
        )
        return dict(body=json_str)

    @staticmethod
    def __serialize_text_plain(in_data: typing.Any) -> typing.Dict[str, str]:
        if isinstance(in_data, frozendict.frozendict):
            raise ValueError('Unable to serialize type frozendict.frozendict to text/plain')
        elif isinstance(in_data, tuple):
            raise ValueError('Unable to serialize type tuple to text/plain')
        elif isinstance(in_data, NoneClass):
            raise ValueError('Unable to serialize type NoneClass to text/plain')
        elif isinstance(in_data, BoolClass):
            raise ValueError('Unable to serialize type BoolClass to text/plain')
        return dict(body=str(in_data))

    def __multipart_json_item(self, key: str, value: Schema) -> RequestField:
        json_value = self.__json_encoder.default(value)
        request_field = RequestField(name=key, data=json.dumps(json_value))
        request_field.make_multipart(content_type='application/json')
        return request_field

    def __multipart_form_item(self, key: str, value: Schema) -> RequestField:
        if isinstance(value, str):
            request_field = RequestField(name=key, data=str(value))
            request_field.make_multipart(content_type='text/plain')
        elif isinstance(value, bytes):
            request_field = RequestField(name=key, data=value)
            request_field.make_multipart(content_type='application/octet-stream')
        elif isinstance(value, FileIO):
            # TODO use content.encoding to limit allowed content types if they are present
            request_field = RequestField.from_tuples(key, (os.path.basename(value.name), value.read()))
            value.close()
        else:
            request_field = self.__multipart_json_item(key=key, value=value)
        return request_field

    def __serialize_multipart_form_data(
        self, in_data: Schema
    ) -> typing.Dict[str, typing.Tuple[RequestField, ...]]:
        if not isinstance(in_data, frozendict.frozendict):
            raise ValueError(f'Unable to serialize {in_data} to multipart/form-data because it is not a dict of data')
        """
        In a multipart/form-data request body, each schema property, or each element of a schema array property,
        takes a section in the payload with an internal header as defined by RFC7578. The serialization strategy
        for each property of a multipart/form-data request body can be specified in an associated Encoding Object.

        When passing in multipart types, boundaries MAY be used to separate sections of the content being
        transferred – thus, the following default Content-Types are defined for multipart:

        If the (object) property is a primitive, or an array of primitive values, the default Content-Type is text/plain
        If the property is complex, or an array of complex values, the default Content-Type is application/json
            Question: how is the array of primitives encoded?
        If the property is a type: string with a contentEncoding, the default Content-Type is application/octet-stream
        """
        fields = []
        for key, value in in_data.items():
            if isinstance(value, tuple):
                if value:
                    # values use explode = True, so the code makes a RequestField for each item with name=key
                    for item in value:
                        request_field = self.__multipart_form_item(key=key, value=item)
                        fields.append(request_field)
                else:
                    # send an empty array as json because exploding will not send it
                    request_field = self.__multipart_json_item(key=key, value=value)
                    fields.append(request_field)
            else:
                request_field = self.__multipart_form_item(key=key, value=value)
                fields.append(request_field)

        return dict(fields=tuple(fields))

    def __serialize_application_octet_stream(self, in_data: BinarySchema) -> typing.Dict[str, bytes]:
        if isinstance(in_data, bytes):
            return dict(body=in_data)
        # FileIO type
        result = dict(body=in_data.read())
        in_data.close()
        return result

    def __serialize_application_x_www_form_data(
        self, in_data: typing.Any
    ) -> SerializedRequestBody:
        """
        POST submission of form data in body
        """
        if not isinstance(in_data, frozendict.frozendict):
            raise ValueError(
                f'Unable to serialize {in_data} to application/x-www-form-urlencoded because it is not a dict of data')
        cast_in_data = self.__json_encoder.default(in_data)
        value = self._serialize_form(cast_in_data, name='', explode=True, percent_encode=True)
        return dict(body=value)

    def serialize(
        self, in_data: typing.Any, content_type: str
    ) -> SerializedRequestBody:
        """
        If a str is returned then the result will be assigned to data when making the request
        If a tuple is returned then the result will be used as fields input in encode_multipart_formdata
        Return a tuple of

        The key of the return dict is
        - body for application/json
        - encode_multipart and fields for multipart/form-data
        """
        media_type = self.content[content_type]
        if isinstance(in_data, media_type.schema):
            cast_in_data = in_data
        elif isinstance(in_data, (dict, frozendict.frozendict)) and in_data:
            cast_in_data = media_type.schema(**in_data)
        else:
            cast_in_data = media_type.schema(in_data)
        # TODO check for and use encoding if it exists
        # and content_type is multipart or application/x-www-form-urlencoded
        if self._content_type_is_json(content_type):
            return self.__serialize_json(cast_in_data)
        elif content_type == 'text/plain':
            return self.__serialize_text_plain(cast_in_data)
        elif content_type == 'multipart/form-data':
            return self.__serialize_multipart_form_data(cast_in_data)
        elif content_type == 'application/x-www-form-urlencoded':
            return self.__serialize_application_x_www_form_data(cast_in_data)
        elif content_type == 'application/octet-stream':
            return self.__serialize_application_octet_stream(cast_in_data)
        raise NotImplementedError('Serialization has not yet been implemented for {}'.format(content_type))